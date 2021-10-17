import math
import os.path
import re
import subprocess
import tempfile

import nltk


class FScore(object):
    def __init__(self, recall, precision, fscore, complete_match, tagging_accuracy=100):
        self.recall = recall
        self.precision = precision
        self.fscore = fscore
        self.complete_match = complete_match
        self.tagging_accuracy = tagging_accuracy

    def __str__(self):
        return (
            f"(Recall={self.recall:.2f}, "
            f"Precision={self.precision:.2f}, "
            f"FScore={self.fscore:.2f}, "
            f"CompleteMatch={self.complete_match:.2f}"
        ) + (
            f", TaggingAccuracy={self.tagging_accuracy:.2f})"
            if self.tagging_accuracy < 100
            else ")"
        )


def evalb(evalb_dir, gold_trees, predicted_trees, ref_gold_path=None):
    assert os.path.exists(evalb_dir)
    evalb_program_path = os.path.join(evalb_dir, "evalb")
    evalb_spmrl_program_path = os.path.join(evalb_dir, "evalb_spmrl")
    assert os.path.exists(evalb_program_path) or os.path.exists(
        evalb_spmrl_program_path
    )

    if os.path.exists(evalb_program_path):
        evalb_param_path = os.path.join(evalb_dir, "nk.prm")
    else:
        evalb_program_path = evalb_spmrl_program_path
        evalb_param_path = os.path.join(evalb_dir, "spmrl.prm")

    assert os.path.exists(evalb_program_path)
    assert os.path.exists(evalb_param_path)

    assert len(gold_trees) == len(predicted_trees)
    for gold_tree, predicted_tree in zip(gold_trees, predicted_trees):
        assert isinstance(gold_tree, nltk.Tree)
        assert isinstance(predicted_tree, nltk.Tree)
        gold_leaves = list(gold_tree.leaves())
        predicted_leaves = list(predicted_tree.leaves())
        assert len(gold_leaves) == len(predicted_leaves)
        assert all(
            gold_word == predicted_word
            for gold_word, predicted_word in zip(gold_leaves, predicted_leaves)
        )

    temp_dir = tempfile.TemporaryDirectory(prefix="evalb-")
    gold_path = os.path.join(temp_dir.name, "gold.txt")
    predicted_path = os.path.join(temp_dir.name, "predicted.txt")
    output_path = os.path.join(temp_dir.name, "output.txt")

    with open(gold_path, "w") as outfile:
        if ref_gold_path is None:
            for tree in gold_trees:
                outfile.write("{}\n".format(tree.pformat(margin=1e100)))
        else:
            # For the SPMRL dataset our data loader performs some modifications
            # (like stripping morphological features), so we compare to the
            # raw gold file to be certain that we haven't spoiled the evaluation
            # in some way.
            with open(ref_gold_path) as goldfile:
                outfile.write(goldfile.read())

    with open(predicted_path, "w") as outfile:
        for tree in predicted_trees:
            # print(tree)
            outfile.write("{}\n".format(tree.pformat(margin=1e100)))

    '''
    new_gold_path = '/ceph/home/chenxuey20/prosody/self-attentive-parser/gold.txt'
    new_predicted_path = '/ceph/home/chenxuey20/prosody/self-attentive-parser/predicted.txt'
    with open(new_gold_path, 'w') as g:
        for tree in gold_trees:
            g.write("{}\n".format(tree.pformat(margin=1e100)))
        g.close()
    with open(new_predicted_path, 'w') as p:
        for tree in predicted_trees:
            p.write("{}\n".format(tree.pformat(margin=1e100)))
        p.close
    '''
    import count_fscore

    fscore = FScore(math.nan, math.nan, math.nan, math.nan)
    fscore.recall, fscore.precision, fscore.fscore, fscore.complete_match = count_fscore.count(gold_path, predicted_path)
    temp_dir.cleanup()
    '''
    command = "{} -p {} {} {} > {}".format(
        evalb_program_path,
        evalb_param_path,
        gold_path,
        predicted_path,
        output_path,
    )
    # EVALB/evalb -p EVALB/nk.prm /tmp/evalb-fxmw8ejp/gold.txt /tmp/evalb-fxmw8ejp/predicted.txt > /tmp/evalb-fxmw8ejp/output.txt
    # print(command)
    subprocess.run(command, shell=True)

    fscore = FScore(math.nan, math.nan, math.nan, math.nan)
    with open(output_path) as infile:
        num = 0
        for line in infile:
            # num+=1
            # print(num,line)
           
            match = re.match(r"Bracketing Recall\s+=\s+(\d+\.\d+)", line)
            # print(match)
            if match:
                fscore.recall = float(match.group(1))
                print(match.group(1))
            match = re.match(r"Bracketing Precision\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.precision = float(match.group(1))
            match = re.match(r"Bracketing FMeasure\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.fscore = float(match.group(1))
            match = re.match(r"Complete match\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.complete_match = float(match.group(1))
            match = re.match(r"Tagging accuracy\s+=\s+(\d+\.\d+)", line)
            if match:
                fscore.tagging_accuracy = float(match.group(1))
                break
    
    success = (
        not math.isnan(fscore.fscore) or fscore.recall == 0.0 or fscore.precision == 0.0
    )

    if success:
        temp_dir.cleanup()
        # print('hhhhhhhh')
    else:
        print("Error reading EVALB results.")
        print("Gold path: {}".format(gold_path))
        print("Predicted path: {}".format(predicted_path))
        print("Output path: {}".format(output_path))
    '''
    return fscore
