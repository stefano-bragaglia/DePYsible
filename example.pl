% Strict rules
bird(X) <- chicken(X).
bird(X) <- penguin(X).
~flies(X) <- penguin(X).

% Facts
chicken(tina).
penguin(tweety).
scared(tina).

% Defeasible knowledge
flies(X) -< bird(X).
flies(X) -< chicken(X), scared(X).
~flies(X) -< chicken(X).
nests_in_trees(X) -< flies(X).
