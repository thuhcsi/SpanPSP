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
           
            with open(ref_gold_path) as goldfile:
                outfile.write(goldfile.read())

    with open(predicted_path, "w") as outfile:
        for tree in predicted_trees:
            
            outfile.write("{}\n".format(tree.pformat(margin=1e100)))

    import count_fscore

    fscore = FScore(math.nan, math.nan, math.nan, math.nan)
    fscore.recall, fscore.precision, fscore.fscore, fscore.complete_match = count_fscore.count(gold_path, predicted_path)
    temp_dir.cleanup()
    
    return fscore
