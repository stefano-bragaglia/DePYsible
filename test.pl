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

% Uncorrelated
animal(X) <- other(_Mute, X).
value(True, -5, 3.14).
string("text", 'text', text).
"STRING"().
