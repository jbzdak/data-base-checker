from operator import attrgetter
from units.unit3.meta.orm import Tag

__author__ = 'jb'

TAGS = [
    Tag("status:student",  "Student"),
    Tag("status:doktorant",  "Doktorant"),
    Tag("status:absolwent",  "Absolwent"),
    Tag("praca:inz",  "Praca Inżynierska"),
    Tag("praca:mgr",  "Praca Magisterska"),
    Tag("praca:dr",  "Praca Doktorska")
]

TAGS = sorted(TAGS, key=attrgetter("key"))

TITLE = [
    "A type-safe big data system applied to a dynamic distributed cache",
    "A balanced knowledge-based cache embedded in an open real-time solution",
    "An integrated binary toolkit applied to an active functional solution",
    "A virtual big data architecture derived from a scalable watermarking protocol",
    "An interactive functional solution for a type-safe proxy theorem prover",
    "A virtual programmable work cluster derived from a synchronized parallelizing compiler",
    "An active binary work cluster embedded in an active cloud-based interface"
    "A parameterized knowledge-based architecture embedded in a type-safe binary network"
]