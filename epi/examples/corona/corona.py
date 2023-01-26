import importlib.resources

import diffrax as dx
import jax.numpy as jnp
import numpy as np
from jax import vmap

from epi import logger
from epi.core.model import (
    ArtificialModelInterface,
    JaxModel,
    VisualizationModelInterface,
)


class Corona(JaxModel, VisualizationModelInterface):
    def __init__(self, delete=False, create=False):
        super().__init__(delete, create)
        self.dataPath = importlib.resources.path(
            "epi.examples.corona", "CoronaData.csv"
        )

    def getDataBounds(self):
        return np.array([[0.0, 4.0], [0.0, 40.0], [0.0, 80.0], [0.0, 3.5]])

    def getParamBounds(self):
        return np.array([[-4.0, 0.0], [-2.0, 2.0], [-1.0, 3.0]])

    def getParamSamplingLimits(self):
        return np.array([[-4.5, 0.5], [-2.0, 3.0], [-2.0, 3.0]])

    def getCentralParam(self):
        return np.array([-1.8, 0.0, 0.7])

    @classmethod
    def forward(cls, logParam):
        param = jnp.power(10, logParam)
        xInit = jnp.array([999.0, 0.0, 1.0, 0.0])

        def rhs(t, x, param):
            return jnp.array(
                [
                    -param[0] * x[0] * x[2],
                    param[0] * x[0] * x[2] - param[1] * x[1],
                    param[1] * x[1] - param[2] * x[2],
                    param[2] * x[2],
                ]
            )

        term = dx.ODETerm(rhs)
        solver = dx.Kvaerno5()
        saveat = dx.SaveAt(ts=[0.0, 1.0, 2.0, 5.0, 15.0])
        stepsize_controller = dx.PIDController(rtol=1e-5, atol=1e-5)

        try:
            odeSol = dx.diffeqsolve(
                term,
                solver,
                t0=0.0,
                t1=15.0,
                dt0=0.1,
                y0=xInit,
                args=param,
                saveat=saveat,
                stepsize_controller=stepsize_controller,
            )
            return odeSol.ys[1:5, 2]

        except Exception as e:
            logger.warning("ODE solution not possible!", exc_info=e)
            return np.array([-np.inf, -np.inf, -np.inf, -np.inf])


class CoronaArtificial(Corona, ArtificialModelInterface):
    def generateArtificialData(
        self, numSamples=ArtificialModelInterface.NUM_ARTIFICIAL_SAMPLES
    ):
        lowerBound = np.array([-1.9, -0.1, 0.6])
        upperBound = np.array([-1.7, 0.1, 0.8])

        trueParamSample = lowerBound + (
            upperBound - lowerBound
        ) * np.random.rand(numSamples, 3)

        artificialData = vmap(self.forward, in_axes=0)(trueParamSample)

        np.savetxt(
            f"Data/{self.getModelName()}Data.csv",
            artificialData,
            delimiter=",",
        )
        np.savetxt(
            f"Data/{self.getModelName()}Params.csv",
            trueParamSample,
            delimiter=",",
        )

    def getParamSamplingLimits(self):
        return np.array([[-2.5, -1.0], [-0.75, 0.75], [0.0, 1.5]])