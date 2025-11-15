from .Interaction import Interaction
from ..Characters.Character import Character


def killed(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur tue la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="killed",
        agency=0.9,        # très assertif/dominant
        communion=-0.9,    # antisocial
        intensity=0.8,     # haute énergie
        physical_contact=0.9,  # contact physique
        valence=-1.0       # très négatif pour la cible
    )


def laughed_at(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur se moque de la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="laughed at",
        agency=0.5,        # moyennement assertif
        communion=-0.4,    # légèrement antisocial
        intensity=0.6,     # énergie modérée
        physical_contact=0.1,  # surtout verbal
        valence=-0.3       # légèrement négatif
    )


def helped(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur aide la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="helped",
        agency=0.3,        # légèrement assertif
        communion=0.8,     # prosocial
        intensity=0.4,     # énergie modérée
        physical_contact=0.2,  # surtout verbal/psychologique
        valence=0.7        # positif pour la cible
    )


def kissed(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur embrasse la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="kissed",
        agency=0.2,        # légèrement assertif
        communion=0.7,     # prosocial
        intensity=0.6,     # énergie modérée à haute
        physical_contact=0.9,  # contact physique intime
        valence=0.8        # positif pour la cible
    )


def insulted(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur insulte la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="insulted",
        agency=0.6,        # assertif
        communion=-0.7,    # antisocial
        intensity=0.7,     # haute énergie
        physical_contact=0.0,  # purement verbal
        valence=-0.6       # négatif pour la cible
    )


def hugged(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur serre la cible dans ses bras."""
    return Interaction(
        actor=actor,
        target=target,
        description="hugged",
        agency=0.1,        # peu assertif
        communion=0.9,     # très prosocial
        intensity=0.5,     # énergie modérée
        physical_contact=0.8,  # contact physique
        valence=0.6        # positif pour la cible
    )


def threatened(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur menace la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="threatened",
        agency=0.8,        # très assertif/dominant
        communion=-0.6,    # antisocial
        intensity=0.7,     # haute énergie
        physical_contact=0.2,  # surtout verbal avec possible intimidation physique
        valence=-0.7       # négatif pour la cible
    )


def praised(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur complimente la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="praised",
        agency=0.2,        # légèrement assertif
        communion=0.6,     # prosocial
        intensity=0.4,     # énergie modérée
        physical_contact=0.0,  # purement verbal
        valence=0.5        # positif pour la cible
    )


def ignored(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur ignore la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="ignored",
        agency=-0.2,       # passif
        communion=-0.3,    # légèrement antisocial
        intensity=0.1,     # très faible énergie
        physical_contact=0.0,  # aucun contact
        valence=-0.2       # légèrement négatif
    )


def comforted(actor: Character, target: Character) -> Interaction:
    """Interaction où l'acteur console la cible."""
    return Interaction(
        actor=actor,
        target=target,
        description="comforted",
        agency=0.1,        # peu assertif
        communion=0.8,     # très prosocial
        intensity=0.3,     # faible énergie
        physical_contact=0.4,  # contact physique modéré
        valence=0.7        # positif pour la cible
    )
