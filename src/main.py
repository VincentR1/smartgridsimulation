from src.Nodes.generators.consumer.simple_consumers import DayOnNightOff
from src.Nodes.generators.grids.simple_grids import SimpleGrid, SimpleGridWurm


def test():
    transport_eff = 0.9
    nr_test_pass = 0
    nr_test_failed = 0

    print("running tests")

    print("negative overflow")
    grid = SimpleGrid(steps=1, number_consumer=2, number_producer=1, transportation_eff=transport_eff)
    return_flow, updated_balance, updated_loss, updated_mineff, settled = grid.start(0)

    if round(updated_balance, 6) != 0.0:
        print("balance should be 0 but is :" + str(updated_balance))
        nr_test_failed += 1
    else:
        nr_test_pass += 1
    expected_loss = 1 - transport_eff ** 2
    if round(updated_loss, 6) != expected_loss:
        print("loss should be: " + str(expected_loss) + " but is : " + str(updated_loss))
        nr_test_failed += 1
    else:
        nr_test_pass += 1

    print("positive overflow")
    grid2 = SimpleGrid(steps=1, number_consumer=1, number_producer=2, transportation_eff=transport_eff)
    return_flow, updated_balance, updated_loss, updated_mineff, settled = grid2.start(0)

    if round(updated_balance, 6) != 0.0:
        print("balance should be 0 but is :" + str(updated_balance))
        nr_test_failed += 1
    else:
        nr_test_pass += 1
    expected_loss = 1 / transport_eff ** 2 - 1
    if round(updated_loss, 6) != expected_loss:
        print("loss should be: " + str(expected_loss) + " but is : " + str(updated_loss))
        nr_test_failed += 1
    else:
        nr_test_pass += 1

    print("With interconecting grid")
    grid3 = SimpleGridWurm(steps=1, number_producer=1, number_consumer=1, number_interconecting_grids=1,
                           transport_eff=transport_eff)
    return_flow, updated_balance, updated_loss, updated_mineff, settled = grid.start(0)

    if round(updated_balance, 6) != 0.0:
        print("balance should be 0 but is :" + str(updated_balance))
        nr_test_failed += 1
    else:
        nr_test_pass += 1

    expected_loss = 1 - transport_eff ** 6
    if round(updated_loss, 6) != expected_loss:
        print("loss should be: " + str(expected_loss) + " but is : " + str(updated_loss))
        nr_test_failed += 1
    else:
        nr_test_pass += 1

    print("Runned " + str(nr_test_pass + nr_test_failed) + " tests")
    print("Number of failed tests=" + str(nr_test_failed))


if __name__ == "__main__":
    test()
