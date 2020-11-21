# Probapy

Module servant aux probabilités.

# Aperçu

```python
from probapy import *


issues = 1, 2, 3, 4, 5, 6

Ω = Ensemble(*issues)
Ω.equirepartie == True

A = Ω.evenement(
    'Obtenir un nombre paire.', 
    lambda i: int(i) % 2 == 0
)
B = Ω.evenement(
    'Obtenir un multiple de 3.',
    lambda i: int(i) % 3 == 0
)

p(A) == 0.5
p(B) == 0.33
p(-B) == 0.66
p(A) + p(-A) == 1 # p(A) + p(Ā)
p(A | B) == 0.67 # p(A∪B)
p(A & B) == 0.17 # p(A∩B)
p(A, B) == 0.33 # pₐ(B)
p(A | B) == p(A) + p(B) - p(A & B)
```