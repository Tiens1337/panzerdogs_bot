from random import randint, uniform


class MatchStats():
    def __init__(self) -> None:
        self.move_distance = 0
        self.boost_distance = 0
        self.dmg_dealt = 0
        self.dmg_received = 0
        self.score = 0

        self.kills = 0
        self.deaths = 0
        self.time_dead = 0

        self.match_score = 0

        self.first_blood = randint(0, 1)

    def update(self):
        self.move_distance += uniform(10, 40)
        self.boost_distance += uniform(0, 10)

        self.dmg_dealt += (randint(15, 60) * 100)
        self.dmg_received += randint(20, 150)

        self.kills = min(self.kills + randint(5, 6), 10)
        self.deaths = randint(0, 1)
        self.time_dead = self.deaths * 5

        self.score = randint(40, 50)

        self.match_score = min(self.kills + randint(0, 2), 10)
