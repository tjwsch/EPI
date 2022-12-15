# from epic.core.plots import plotTest
from epic.core.sampling import (
    concatenateEmceeSamplingResults,
    runEmceeSampling,
)
from epic.example_models.extern_model import Plant


def test_extern_model():
    # define the model
    model = Plant()  # Behaves just like plant model and uses same data

    # generate artificial data
    model.generateArtificialData()

    # choose the number of subsequent runs
    # after each sub-run, chains are saved
    numRuns = 2

    # choose how many parallel processes can be used
    numProcesses = 4

    # choose how many parallel chains shall be initiated
    numWalkers = 10

    # choose how many steps each chain shall contain
    numSteps = 2500

    # run MCMC sampling for EPI
    runEmceeSampling(model, numRuns, numWalkers, numSteps, numProcesses)

    # combine all intermediate saves to create one large sample chain
    concatenateEmceeSamplingResults(model)

    # plot the results
    # TODO: Write a good general plotting function
