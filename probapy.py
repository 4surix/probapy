# coding: utf-8
# Python 3.6.2 / 3.8.5
# ----------------------------------------------------------------------------

__version__ = '0.0.1'


from typing import Union, Callable, Tuple, Any, Dict


class Ensemble:

    def __init__(
            self, 
            *issues:Tuple[Any], 
            **issues_probabilites:Dict[str, int]
        ):

        if issues_probabilites:

            for issue, probabilite in issues.items():
                if not isinstance(probabilite, float):
                    raise

            assert sum(issues.values()) == 1

            issues = issues_probabilites

        else:

            probabilite = 1 / len(issues)

            issues = {
                str(issue): probabilite
                for issue in issues
            }

        self.issues = issues

    def __str__(self):

        return '{' + ', '.join(self.issues) + '}'

    @property
    def equirepartie(self) -> bool:

        probabilites = list(self.issues.values())

        v = probabilites.pop(0)

        for probabilite in probabilites:
            if probabilite != v:
                return False

        return True

    def evenement(self, commentaire:str, fonction:Callable):

        return Evenement(commentaire, fonction, self)


class Evenement:

    def __init__(self, commentaire:str, fonction:Callable, ensemble:Ensemble):

        self.commentaire = commentaire
        self.fonction = fonction
        self.ensemble = ensemble
        self.issues = {}

        for issue, probabilite in ensemble.issues.items():
            if fonction(issue):
                self.issues[issue] = probabilite

    def __str__(self):

        return '{' + ', '.join(self.issues) + '}'

    def __neg__(self):

        commentaire = self.commentaire.lower()

        return Evenement(
            (
                commentaire[7:].capitalize() if commentaire[:7] == 'ne pas '
                else
                    'Ne pas ' + commentaire
            ),
            lambda v: not self.fonction(v),
            self.ensemble
        )

    def __or__(self, evenement):

        return Union(self, evenement)

    def __and__(self, evenement):

        return Inter(self, evenement)

    @property
    def impossible(self):

        return p(self) == 0

    @property
    def certain(self):

        return p(self) == 1


class Union:

    def __init__(self, A:Evenement, B:Evenement):

        self.issues = {**A.issues, **B.issues}

    def __str__(self):

        return '{' + ', '.join(self.issues) + '}'


class Inter:

    def __init__(self, A:Evenement, B:Evenement):

        self.issues = {}

        for issue, probabilite in A.issues.items():
            if issue in B.issues:
                self.issues[issue] = probabilite

        for issue, probabilite in B.issues.items():
            if issue in A.issues:
                self.issues[issue] = probabilite

    def __str__(self):

        return '{' + ', '.join(self.issues) + '}'
    

def p(evenement:Evenement, evenement_cond:Evenement = None) -> float:
    return round(
        # p(B)
        sum(evenement.issues.values()) if not evenement_cond
        # pₐ(B)
        else
            # p(B∩A)
            sum(
                probabilite
                for issue, probabilite in evenement_cond.issues.items()
                if issue in evenement.issues
            )

            /
            
            # p(A)
            sum(evenement.issues.values())
        ,
        100
    )