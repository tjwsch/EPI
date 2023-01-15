# from epic.core.plots import plotTest
from epic.core.sampling import (
    concatenateEmceeSamplingResults,
    runEmceeSampling,
)
from epic.example_models.autodiff import AutodiffPlantModel


def test_autodiff_model():
    # define the model
    model = (
        AutodiffPlantModel()
    )  # Behaves just like plant model and uses same data

    # generate artificial data
    model.generateArtificialData()

    # run MCMC sampling for EPI
    runEmceeSampling(model)

    # combine all intermediate saves to create one large sample chain
    concatenateEmceeSamplingResults(model)

    # plot the results
    # TODO: Write a good general plotting function
