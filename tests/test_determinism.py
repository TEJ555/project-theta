import unittest

from project_theta.body import SyntheticBody
from project_theta.config import BodyConfig, WorldConfig
from project_theta.world import GridWorld


class DeterminismTests(unittest.TestCase):
    def trajectory(self, seed: int):
        world_config = WorldConfig()
        world = GridWorld(world_config, seed)
        body = SyntheticBody(BodyConfig(), world_config, seed)
        output = []
        for action in ("east", "east", "south", "wait", "north", "east"):
            signal, delta = body.sense(world.tick)
            events, reward = world.step(action)
            body.update(events)
            output.append((world.hidden_state(), body.hidden_state(), signal, delta, reward))
        return output

    def test_same_seed_replays_exactly(self):
        self.assertEqual(self.trajectory(17), self.trajectory(17))

    def test_counterbalance_changes_map(self):
        odd = GridWorld(WorldConfig(), 11).hidden_state()["hazards"]
        even = GridWorld(WorldConfig(), 12).hidden_state()["hazards"]
        self.assertNotEqual(odd, even)


if __name__ == "__main__":
    unittest.main()

