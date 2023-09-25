import unittest
import os
import numpy as np
import subprocess
import time

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TMultiplexedProtocol

from whatsopt_server.services import ttypes as SensitivityAnalysisTypes
from whatsopt_server.services import SensitivityAnalyser, Administration


class SensitivityAnalyserProxy(object):
    def __init__(self):
        self.transport = transport = TSocket.TSocket("localhost", 41400)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        multiplex1 = TMultiplexedProtocol.TMultiplexedProtocol(
            protocol, "SensitivityAnalyserService"
        )
        self._thrift_client = SensitivityAnalyser.Client(multiplex1)
        multiplex2 = TMultiplexedProtocol.TMultiplexedProtocol(
            protocol, "AdministrationService"
        )
        self._admin_client = Administration.Client(multiplex2)
        transport.open()

    def ping(self):
        return self._admin_client.ping()

    def compute_hsic(self, thresholding_type, xdoe, ydoe, quantile, g_threshold):
        return self._thrift_client.compute_hsic(thresholding_type, xdoe, ydoe, quantile, g_threshold)

    def close(self):
        self.transport.close()


class TestSurrogateService(unittest.TestCase):
    def setUp(self):
        cmd = os.path.join(
            os.path.dirname(__file__), os.path.pardir, "whatsopt_server", "__main__.py"
        )
        self.server = subprocess.Popen(["python", cmd])
        for _ in range(10):
            try:
                self.analyser = SensitivityAnalyserProxy()  # server has to start
            except TTransport.TTransportException:
                time.sleep(0.5)
                continue
            else:
                break

    def tearDown(self):
        self.analyser.close()
        self.server.kill()

    def test_compute_hsic(self):
        xdoe = [
            [6.01569341e-01, 8.54602233e-01, 6.20265381e-01, 9.87681078e-01, 2.11042512e-01],
            [1.64381332e-01, 3.99379700e-01, 1.74711842e-02, 6.01670715e-01, 7.69706697e-01],
            [4.79670684e-01, 2.83668349e-01, 9.39577876e-01, 6.49827337e-03, 8.85201557e-01],
            [8.70745292e-02, 1.00669771e-01, 3.57460596e-01, 6.12316065e-01, 4.29817215e-01],
            [5.12121032e-01, 1.48994428e-01, 8.70739946e-01, 2.09211665e-01, 4.28357206e-02],
            [8.83279736e-01, 9.04624680e-01, 8.09635483e-03, 1.77513894e-01, 5.75607808e-01],
            [4.42731945e-01, 9.13219468e-01, 4.22420268e-01, 1.17956287e-01, 5.60750639e-01],
            [9.85870182e-01, 5.57364342e-01, 1.56975754e-01, 3.59689566e-01, 3.89015879e-01],
            [1.07716726e-01, 2.14080096e-01, 6.52283948e-02, 3.06256415e-01, 9.54932393e-01],
            [5.80027862e-01, 6.55548063e-01, 6.03213894e-01, 2.48951219e-01, 3.04712103e-01],
            [7.41093359e-01, 8.91425927e-01, 3.63392108e-01, 8.90039670e-01, 7.37069175e-01],
            [9.75993130e-01, 4.10770331e-01, 5.01481025e-01, 9.54260917e-01, 6.55526949e-01],
            [1.78539856e-01, 2.61300600e-02, 2.16745008e-01, 7.66676080e-01, 8.43161555e-01],
            [4.37716593e-01, 9.05648351e-01, 8.19724529e-01, 5.50436278e-01, 7.41266255e-01],
            [3.14516481e-01, 1.25051250e-01, 7.12987238e-02, 6.56455581e-01, 4.93483106e-01],
            [9.53344199e-01, 5.21166322e-01, 8.33110101e-02, 8.46525265e-01, 7.19061270e-01],
            [7.16305082e-01, 8.65790697e-01, 7.14546547e-01, 3.46931879e-01, 6.87662020e-01],
            [9.55404449e-01, 7.93509887e-01, 4.63268059e-01, 5.97920890e-01, 7.31550875e-01],
            [2.41903963e-01, 4.39806951e-01, 6.86936146e-01, 7.11093734e-01, 9.30789066e-01],
            [5.01332949e-01, 2.40891549e-01, 4.37784844e-01, 7.60377499e-01, 4.11589492e-01],
            [1.37747484e-01, 8.15849683e-01, 5.25700921e-01, 6.90887910e-01, 1.36160591e-01],
            [9.37497287e-01, 7.27515107e-01, 6.47946898e-01, 1.41087012e-01, 3.26724900e-01],
            [4.10171377e-01, 2.49902425e-01, 2.69915692e-01, 5.16529586e-01, 3.17670509e-01],
            [8.03363112e-01, 5.64377107e-01, 9.69942862e-01, 7.00811548e-01, 8.98191810e-01],
            [4.58128943e-01, 1.62161945e-01, 4.31120007e-01, 7.74552609e-01, 6.33413638e-03],
            [4.93854890e-01, 2.85367492e-01, 7.85599403e-01, 5.36214795e-01, 7.63469440e-02],
            [5.72228511e-01, 9.42301275e-01, 2.43908297e-01, 9.01013253e-01, 2.57147943e-01],
            [4.71377298e-02, 3.26267741e-01, 3.00479367e-01, 4.34705912e-01, 7.23799593e-01],
            [6.15607993e-01, 4.71837363e-02, 6.57353574e-01, 5.04209338e-01, 3.48055447e-01],
            [1.30476440e-01, 2.60436896e-01, 9.02203473e-01, 2.92317246e-01, 1.17446331e-01],
            [8.68655477e-01, 2.03264325e-02, 3.74519231e-01, 5.26202821e-01, 5.04620076e-01],
            [5.60905607e-01, 6.30090856e-02, 8.01395500e-01, 8.98645534e-02, 3.91243671e-01],
            [7.33972356e-01, 3.51625284e-01, 4.09062528e-01, 4.43396630e-01, 4.19181246e-01],
            [9.46993123e-01, 6.05263749e-01, 2.52308695e-01, 3.24153492e-02, 9.10731787e-02],
            [7.67389830e-01, 3.70492343e-01, 4.72175613e-01, 4.74563386e-01, 6.72067746e-02],
            [2.70438938e-01, 3.30314508e-01, 6.31621975e-01, 2.60508724e-01, 7.47350048e-01],
            [6.76203344e-02, 7.16177066e-02, 8.22167615e-01, 4.64396435e-01, 8.45431332e-01],
            [8.60922521e-01, 8.76349244e-01, 7.69911323e-01, 5.46750527e-01, 2.06357999e-02],
            [7.72297456e-01, 6.80594740e-01, 6.62346339e-01, 7.86292662e-01, 9.91668359e-01],
            [3.81632942e-01, 6.79116069e-01, 3.05630801e-01, 2.31143051e-01, 9.86837581e-01],
            [2.96303600e-01, 3.36030488e-01, 8.91626341e-01, 4.65328553e-01, 5.56531616e-01],
            [7.86837353e-02, 4.24560094e-01, 5.15703707e-01, 6.48644532e-01, 4.72849883e-01],
            [2.79837265e-02, 2.72794754e-01, 5.34648685e-01, 4.02476810e-01, 2.02089181e-01],
            [8.91126559e-01, 1.39225566e-01, 8.42789305e-01, 3.74111562e-01, 7.77714615e-01],
            [6.25697085e-01, 5.62358862e-02, 3.32020336e-02, 2.17845703e-01, 6.76079581e-01],
            [2.63209059e-01, 6.30263148e-01, 4.02697305e-01, 2.61015310e-02, 7.81903586e-01],
            [2.25262305e-02, 3.08645004e-01, 8.34406473e-01, 1.52948910e-01, 7.59503490e-01],
            [7.39325722e-01, 5.04104746e-02, 3.54648952e-01, 7.89870247e-02, 5.39768458e-01],
            [1.69768300e-01, 2.97013190e-01, 8.54271773e-01, 7.22997896e-01, 1.48523137e-01],
            [4.32817130e-01, 5.73389717e-01, 4.41842016e-01, 4.87959395e-01, 2.28598438e-01],
            [3.96448377e-01, 8.41012122e-01, 1.06728997e-02, 7.36629454e-01, 5.20313752e-02],
            [5.97899254e-01, 5.14220460e-01, 4.87707383e-01, 9.14544144e-01, 6.83524374e-01],
            [9.73601290e-01, 3.62525310e-01, 2.10656973e-01, 5.78239203e-01, 6.22213005e-01],
            [9.93226970e-01, 2.55878621e-01, 7.79317971e-01, 2.00023318e-01, 5.98529016e-02],
            [8.38667260e-01, 4.87968702e-01, 2.55396191e-01, 6.43993563e-01, 2.33131720e-01],
            [7.13171194e-01, 9.63126102e-01, 8.62248695e-01, 8.52456282e-01, 8.36417733e-01],
            [2.88204693e-01, 7.14152365e-01, 7.02395041e-01, 2.42361043e-01, 9.80279667e-01],
            [8.45052561e-01, 6.45505550e-01, 8.99549130e-01, 4.80926220e-01, 2.39275598e-01],
            [9.68122237e-01, 4.33703510e-01, 9.91164614e-01, 2.95075281e-01, 5.54180929e-01],
            [3.25047252e-01, 6.29943712e-01, 6.09479269e-01, 2.86766069e-01, 5.87311688e-01],
            [6.14493497e-01, 6.67652344e-01, 1.51785675e-01, 6.28098165e-01, 2.67491314e-02],
            [9.10804772e-01, 1.82407291e-01, 2.08387924e-01, 3.67142701e-01, 9.09409554e-01],
            [4.17860044e-01, 9.45421851e-01, 1.83741870e-01, 5.94959626e-01, 4.60016677e-01],
            [3.41617643e-01, 3.88471196e-01, 4.19547650e-01, 7.19344494e-02, 1.25936433e-01],
            [5.32531274e-01, 6.61000982e-01, 6.17893739e-01, 4.54869338e-01, 9.04978285e-01],
            [5.25319625e-01, 5.17118245e-01, 9.26069400e-01, 4.79910394e-01, 4.42820539e-01],
            [4.96938195e-01, 7.84357495e-01, 9.53058922e-01, 7.47248711e-01, 4.22883548e-01],
            [9.97992523e-01, 2.21028968e-01, 2.97183349e-01, 8.20097694e-01, 8.66215912e-01],
            [6.22649019e-01, 7.65898529e-01, 2.01094104e-01, 3.13340497e-01, 5.95982586e-01],
            [5.09892918e-01, 5.40017867e-01, 2.21406116e-02, 3.18466669e-01, 3.96706050e-01],
            [6.81726078e-01, 4.43721804e-01, 6.91431101e-01, 6.52752727e-01, 3.30348303e-01],
            [1.89243423e-01, 7.98583977e-01, 9.36919988e-02, 9.37474606e-01, 3.68145047e-01],
            [1.94702252e-01, 7.68960528e-02, 7.42202061e-01, 4.92248125e-01, 3.36456689e-01],
            [5.37371526e-01, 9.94660253e-01, 7.36077841e-01, 3.61663800e-01, 3.12515034e-01],
            [6.74530867e-01, 9.16515231e-01, 4.44476003e-02, 8.19376171e-02, 2.67388682e-01],
            [2.25535937e-01, 9.57839450e-01, 7.25368305e-01, 6.32348863e-01, 4.59701988e-01],
            [2.14705579e-01, 5.07071655e-01, 2.84376344e-01, 5.59694844e-01, 1.53982274e-02],
            [7.29350129e-01, 5.66157374e-01, 3.76543045e-01, 2.11733150e-01, 8.05486954e-01],
            [9.15662926e-02, 6.13378116e-01, 7.52202224e-01, 9.74729886e-01, 6.30568170e-01],
            [7.20235648e-01, 4.08931143e-01, 5.53357219e-02, 4.25492750e-01, 7.09506601e-01],
            [6.33908372e-01, 2.02530434e-01, 5.36546986e-01, 2.84757551e-01, 6.50974246e-01],
            [5.50684812e-01, 7.35901953e-01, 7.57507379e-01, 5.66668233e-01, 1.79783738e-01],
            [2.79166062e-01, 8.58223052e-01, 3.19760054e-01, 9.28164685e-01, 3.25261836e-02],
            [5.67223409e-01, 9.02089885e-02, 1.04344583e-01, 3.00984822e-01, 1.55990136e-01],
            [8.41707848e-01, 9.80372890e-01, 3.37321062e-01, 3.37073341e-01, 9.27630469e-01],
            [3.00145747e-01, 1.99629508e-01, 3.68928989e-01, 4.17080683e-02, 9.19467967e-01],
            [9.27398021e-01, 4.64275500e-01, 4.29307004e-01, 1.46147870e-01, 5.08721279e-01],
            [3.68878990e-01, 4.90445251e-01, 9.98401957e-01, 8.07098845e-01, 9.14502458e-01],
            [4.69623941e-01, 5.29062588e-01, 5.96918146e-01, 7.79621597e-01, 3.85037617e-02],
            [6.77393224e-01, 1.78887940e-01, 5.66794308e-01, 3.58114930e-02, 9.74006876e-01],
            [1.72538087e-01, 4.02814287e-01, 2.74831239e-03, 4.46688598e-01, 2.84261315e-01],
            [8.85332953e-01, 6.24288882e-01, 7.91912639e-01, 5.43500989e-01, 6.71430311e-01],
            [9.08619717e-01, 6.37671073e-01, 7.22409644e-01, 1.58342135e-01, 7.13697673e-01],
            [1.96941671e-01, 8.47028671e-01, 7.60437532e-01, 6.63063795e-01, 9.98964213e-01],
            [8.95065010e-01, 7.19692155e-01, 6.25991263e-01, 8.95790976e-01, 4.66586417e-01],
            [5.19230539e-01, 4.72620657e-01, 5.58124562e-01, 5.71611909e-01, 6.06620166e-01],
            [1.89266757e-02, 4.95255286e-01, 5.50507441e-01, 3.91327217e-01, 8.64188869e-01],
            [3.59771443e-01, 8.22217363e-01, 8.80529313e-01, 9.06531271e-01, 8.16991301e-01],
            [6.47249169e-01, 1.18117816e-01, 9.14787908e-01, 6.20565257e-01, 5.74991398e-01],
            [1.22739539e-01, 9.73447997e-01, 3.85698817e-01, 5.14094578e-01, 4.53490997e-01],
            [4.50305769e-01, 5.89606624e-01, 6.14958356e-01, 8.33877606e-01, 3.55672134e-01],
            [5.27210408e-02, 9.35769817e-01, 4.13740925e-01, 1.20933136e-01, 4.01503765e-01],
            [5.51360118e-02, 5.48510811e-01, 3.30489802e-01, 1.91416294e-01, 8.24853690e-02],
            [1.55328318e-01, 7.22997000e-01, 1.39942549e-01, 4.24792570e-01, 6.02124181e-01],
            [7.60085704e-01, 8.08840469e-01, 4.75925901e-01, 1.92328074e-02, 7.00343438e-01],
            [1.48265103e-01, 6.86217754e-01, 4.83182817e-01, 4.37658342e-01, 3.71876907e-01],
            [7.55631163e-01, 9.82192097e-02, 2.63578653e-01, 6.72670073e-01, 2.19025658e-01],
            [2.19336908e-01, 6.72547401e-01, 8.29034713e-01, 1.03743889e-01, 2.48811676e-01],
            [8.30351288e-01, 7.44598552e-01, 9.24860167e-01, 8.77702795e-01, 5.91504409e-01],
            [4.88271210e-01, 9.85970550e-01, 5.08865933e-01, 8.04463891e-01, 8.23594958e-01],
            [3.20217448e-01, 8.67543595e-02, 8.13486147e-01, 7.15801062e-01, 6.95477588e-01],
            [2.94465831e-01, 1.87222855e-01, 5.80415142e-01, 9.99265999e-01, 2.92446506e-01],
            [7.07462557e-01, 3.16686841e-01, 7.50650867e-02, 6.95562677e-01, 9.47002814e-01],
            [8.20707179e-01, 2.69426318e-01, 7.49946676e-01, 3.25853428e-01, 3.61531823e-01],
            [5.91698696e-01, 4.16862103e-01, 6.79379965e-01, 9.32875619e-02, 6.66280107e-01],
            [4.23008819e-01, 9.77482754e-01, 2.31653735e-01, 2.79974751e-01, 2.41297402e-01],
            [3.73527515e-01, 6.67831214e-02, 1.66035249e-01, 8.83341318e-01, 1.85126007e-01],
            [1.19131249e-01, 3.46557647e-01, 8.56610138e-01, 7.54765742e-01, 4.82896010e-01],
            [9.18317944e-01, 8.80143394e-01, 3.24715854e-01, 4.56856175e-01, 1.63076273e-01],
            [3.61224971e-01, 4.51863857e-01, 9.32694045e-01, 9.58523857e-02, 5.47297360e-01],
            [1.11318893e-01, 1.23497603e-01, 1.44350729e-01, 6.16084047e-01, 1.03992928e-01],
            [3.16890012e-01, 8.37833317e-01, 4.57175462e-01, 8.29104088e-01, 4.88544956e-01],
            [5.41987052e-01, 1.90510690e-01, 4.65774678e-01, 5.05840266e-01, 9.77847057e-01],
            [6.64277715e-01, 1.55217506e-01, 6.44664926e-01, 8.65009620e-01, 1.82072300e-01],
            [3.06856356e-01, 3.01864464e-01, 3.92864061e-01, 2.17661196e-03, 5.18546810e-01],
            [7.88002048e-01, 5.34254660e-01, 6.39134043e-01, 1.99583573e-01, 1.09221993e-02],
            [3.48222631e-01, 2.33849298e-01, 3.79000209e-02, 1.35244340e-01, 5.44076352e-01],
            [1.26370296e-01, 7.09515727e-01, 9.49571686e-01, 8.42241718e-01, 2.52681717e-01],
            [3.23389374e-02, 7.52161015e-01, 9.07641033e-01, 4.16934856e-01, 5.10361627e-01],
            [8.06240141e-01, 2.09382809e-01, 6.38247993e-02, 3.84821834e-01, 3.43446259e-01],
            [5.89830571e-01, 8.10527122e-01, 4.47379944e-01, 5.87281160e-01, 6.61348061e-01],
            [1.81659369e-01, 1.40807333e-01, 7.34513160e-01, 9.77624752e-01, 8.51720925e-01],
            [8.55011045e-01, 4.28694354e-01, 5.61517929e-01, 3.86333129e-01, 9.20859025e-01],
            [6.65167411e-03, 7.01035433e-01, 2.55347284e-02, 7.44759130e-01, 9.40634742e-01],
            [3.69344633e-02, 5.78814307e-01, 1.88578735e-01, 6.83155057e-01, 4.79992516e-01],
            [3.85810917e-01, 5.36452291e-01, 1.93309839e-01, 7.83252162e-01, 3.54205615e-01],
            [1.03890041e-01, 1.14569577e-01, 2.79944310e-01, 5.99692601e-02, 6.46139764e-01],
            [7.54703345e-01, 4.77880772e-01, 9.15374516e-01, 1.31428019e-01, 2.85823893e-01],
            [9.23539547e-01, 3.81101449e-01, 5.94079898e-01, 8.71405867e-01, 2.60877995e-01],
            [7.00060256e-01, 6.95909758e-01, 2.26104406e-01, 2.50628907e-01, 1.72251136e-01],
            [5.22231425e-01, 4.25000418e-02, 8.36382473e-01, 2.72572010e-01, 8.58110926e-01],
            [8.70685353e-01, 1.50152947e-01, 7.05057504e-01, 2.04826546e-02, 4.97763900e-01],
            [1.43216557e-01, 1.72628666e-01, 1.70212146e-01, 1.70822095e-01, 2.73044651e-01],
            [9.41599380e-01, 4.69756469e-01, 8.77548895e-02, 6.99157672e-02, 6.93615629e-01],
            [2.02506082e-01, 2.18961651e-01, 6.73506710e-01, 5.42542525e-02, 3.09406176e-01],
            [4.25138721e-01, 4.55779723e-01, 3.26271133e-01, 7.33172190e-01, 9.62006244e-01],
            [3.52615847e-01, 3.89681873e-02, 9.71356780e-01, 9.15859282e-01, 1.98511321e-01],
            [8.11110807e-01, 7.30606194e-01, 4.94567477e-01, 7.92524308e-01, 6.14651162e-02],
            [2.83470763e-01, 8.96502817e-01, 7.72866679e-01, 9.61891683e-01, 5.30513746e-01],
            [4.07557244e-01, 6.02324317e-03, 9.59516275e-01, 3.40585525e-01, 5.25069519e-01],
            [9.60655908e-01, 1.29631159e-04, 6.67224084e-01, 6.37211425e-01, 2.99464529e-01],
            [6.38205887e-01, 6.41178250e-01, 2.46231268e-01, 5.23465866e-01, 9.66322578e-01],
            [2.68566608e-01, 8.87258433e-01, 4.98318206e-01, 2.24017071e-01, 4.97687111e-02],
            [7.25200022e-02, 7.59707282e-01, 1.63098207e-01, 6.08637373e-01, 1.50261114e-01],
            [9.70837672e-02, 3.92985083e-01, 3.81636971e-01, 8.56955010e-01, 7.64711296e-01],
            [4.46039875e-01, 1.31418779e-01, 5.21193827e-01, 9.44491720e-01, 7.74900431e-01],
            [7.91722820e-01, 2.76618753e-01, 2.88116924e-01, 9.49082779e-01, 4.48313176e-01],
            [9.31370587e-01, 3.11438176e-01, 2.23653401e-01, 8.88366715e-01, 9.94082612e-02],
            [2.07816881e-01, 8.62805658e-01, 3.49401495e-01, 6.66815793e-01, 8.80512850e-01],
            [8.77366930e-01, 8.71706865e-01, 8.86823707e-01, 7.97327207e-01, 2.79130754e-01],
            [4.72927777e-01, 2.94124452e-01, 2.38212262e-01, 3.32483638e-01, 8.03221372e-01],
            [5.55844738e-01, 7.49008009e-01, 8.69558140e-01, 4.76780209e-02, 5.23238847e-01],
            [7.78478635e-01, 1.06104190e-01, 5.87916322e-01, 8.13738154e-01, 6.41717291e-01],
            [6.58974991e-01, 3.65164270e-01, 8.45187757e-01, 3.95458182e-01, 8.92754414e-01],
            [4.48227554e-02, 5.01019380e-01, 6.84941276e-01, 2.55994495e-01, 4.33216642e-01],
            [6.87153690e-01, 6.53374238e-01, 1.15883561e-01, 9.22549462e-01, 3.21787591e-01],
            [6.40012918e-02, 5.52136887e-01, 6.52213218e-01, 9.56982602e-01, 2.20215645e-01],
            [4.82232341e-01, 5.83727766e-01, 9.80900400e-01, 8.38603237e-01, 1.13042211e-01],
            [6.97085133e-01, 2.54194513e-01, 5.71504284e-01, 1.25678906e-02, 1.06731190e-01],
            [6.06902831e-01, 1.92698765e-02, 1.78885515e-01, 7.56803531e-01, 6.27218285e-01],
            [5.76191370e-01, 4.47734070e-01, 2.92633192e-01, 1.26475862e-01, 3.80480454e-01],
            [7.47342763e-01, 9.96794601e-01, 5.42476311e-01, 1.67126836e-01, 1.91004212e-01],
            [6.52210077e-01, 9.26995911e-01, 6.98021735e-01, 1.61452134e-01, 9.56273133e-01],
            [3.39675768e-01, 5.94836767e-01, 1.09592293e-01, 2.68264535e-01, 7.41600845e-02],
            [4.62264088e-01, 9.34013861e-01, 9.83074066e-02, 7.29568820e-01, 7.87231186e-01],
            [2.50600199e-01, 6.94158918e-01, 8.75339891e-01, 5.81213596e-01, 2.10183901e-03],
            [6.67398318e-01, 6.00674734e-01, 1.97851371e-01, 6.79703977e-01, 6.36475104e-01],
            [2.33565036e-01, 7.76841529e-01, 1.28146799e-01, 9.82439025e-01, 7.25303909e-01],
            [3.91503059e-01, 4.83812153e-01, 1.12098677e-01, 4.96828303e-01, 6.17737979e-01],
            [2.48461996e-01, 3.10087161e-02, 5.10985101e-01, 2.29403110e-01, 8.55638811e-02],
            [6.41579461e-01, 6.18732358e-01, 9.75461478e-01, 1.84289198e-01, 8.31276847e-01],
            [6.94081105e-01, 3.75314027e-01, 8.07684045e-01, 9.66494671e-01, 5.68124438e-01],
            [3.31013245e-01, 7.71839667e-01, 5.18317120e-02, 1.07960423e-01, 3.79065909e-01],
            [5.48766934e-01, 3.55012412e-01, 4.88827959e-02, 8.19459578e-01, 1.20552916e-01],
            [2.37072396e-01, 7.86215911e-01, 9.87145519e-01, 3.78565960e-01, 7.97969780e-01],
            [7.95445131e-01, 1.26457105e-02, 3.95093791e-01, 6.86443442e-01, 9.39563654e-01],
            [9.02282700e-01, 2.39683905e-01, 7.96120552e-01, 7.06140391e-01, 8.72002271e-01],
            [8.52727697e-01, 3.21237754e-01, 9.61055104e-01, 8.61882734e-01, 2.09630806e-01],
            [4.01101508e-01, 3.41057988e-01, 1.45156238e-01, 9.31697178e-01, 6.10548039e-01],
            [2.24165806e-01, 7.64738125e-01, 5.45990478e-01, 9.94950101e-01, 8.12178734e-01],
            [8.28287190e-01, 9.20521794e-01, 5.78497933e-01, 5.32316549e-01, 4.09031676e-01],
            [2.56482564e-01, 8.01277547e-02, 4.52170547e-01, 3.54241007e-01, 8.26070735e-01],
            [1.50437813e-01, 8.27932922e-01, 7.83422407e-01, 6.08461272e-02, 7.52484440e-01],
            [1.31056692e-02, 5.98410339e-01, 2.70905751e-01, 1.12700958e-01, 5.84946138e-01],
            [2.17997451e-03, 8.02073715e-01, 3.14835566e-01, 3.22784301e-01, 8.78166923e-01],
            [9.80906678e-01, 2.27175418e-01, 3.41401341e-01, 1.85042242e-01, 1.43708775e-01],
            [7.83557754e-01, 8.31843879e-01, 1.31074622e-01, 5.61388265e-01, 4.35223835e-01],
            [3.75973972e-01, 9.69776326e-01, 1.21229056e-01, 2.36934502e-01, 7.91454279e-01],
            [8.29134244e-02, 9.52715194e-01, 7.19785748e-01, 4.11924349e-01, 1.67222871e-01],
            [8.15271472e-01, 1.67240074e-01, 9.42606828e-01, 4.07664204e-01, 1.32357049e-01]
        ]

        ydoe = [[329.3586812977305, 651.4177536874938, 344.71194829685004, 772.7905710895651, 336.12139015077804, 236.06323749010122, 509.168283446047, 221.267934884755, 723.7951113545107, 272.6006246780713, 207.6026551855396, 202.45387760879527, 707.9515940412631, 511.24476423701816, 539.8522831551085, 186.52826074247534, 215.8025276154067, 259.4236637814204, 576.8138819094548, 330.32852844185715, 766.7760646223207, 215.86281388659677, 417.79516513165277, 40.04363030074323, 388.7022391880424, 330.64802661844993, 401.15883287932627, 769.6637758578885, 264.14238210108635, 693.7596226763101, 158.58161173070187, 313.2002203332662, 86.46410642994006, 191.43947084608675, 52.879536310221084, 547.9219580670721, 800.9057267000239, 200.80983418409832, 92.42086321415674, 475.1131865497272, 521.7924930490325, 737.2589166940982, 794.1276272833531, 144.00470619873028, 250.19785211739483, 580.372368824041, 795.8524074707802, 139.55416347450583, 652.2732926810213, 400.41426076521697, 522.1759446010318, 231.79157271795572, 196.25739973744334, 224.30930551762316, 64.90799397396802, 273.3499909388352, 578.816682257685, 98.13109225250899, 190.23946595051373, 518.7763923658512, 242.82517016454378, 153.58017374332044, 552.0758100519897, 475.0671873016026, 321.49584209564466, 300.24193701245815, 399.1351791423701, 236.86177540705208, 265.2416219809429, 318.1309005806472, 140.46570384464223, 711.289304064673, 673.0865494435643, 461.93984120406185, 281.94391537655974, 749.8737965718623, 607.3430612466009, 104.87546187254272, 751.3915595436797, 99.26083154080814, 203.18839522353574, 327.1512477085002, 648.210304715154, 297.3570338845444, 235.96697797405426, 536.0061059554376, 151.02577082337044, 454.76727462068663, 359.50118540593314, 165.57574263154757, 642.6281458950327, 134.29398497417876, 160.3710995568287, 721.9358459367488, 174.6991328587514, 302.43842474589684, 799.8260797723077, 552.2030121565587, 210.66358571979487, 859.0857253212521, 389.2946664982177, 906.9208869499854, 770.3481215415475, 712.906433523289, 146.87407470506173, 708.6360349492012, 108.86456520929298, 634.5895159565998, 117.08226030786338, 507.836761377268, 546.0988187591795, 548.7217724174373, 116.29722253508007, 48.85993905625447, 227.57054184028144, 563.9907482124629, 500.80734039552345, 699.0255191771679, 259.84187957664426, 457.0246173661473, 742.1374018209451, 600.3932463232939, 297.23748166838084, 186.8718713306469, 514.4690199179047, 42.2632372350371, 481.60083977240765, 740.3258348507117, 844.7508598993292, 43.09057446506286, 316.5682982381163, 671.6065425905459, 76.29041791688499, 855.1729823456985, 794.9037520666842, 443.22499020101793, 751.7590645143165, 68.54343604544574, 148.54006149687672, 164.8868801760972, 358.1089658788964, 121.83042081565189, 697.273363081064, 165.97735244262756, 629.9111942608272, 395.5418177045599, 531.5504483919485, 91.74233628922231, 663.3869386347295, 485.7019804890301, 259.3331637783115, 211.678505435579, 668.1339570431845, 808.5259872213579, 720.4664174753273, 410.3133781856335, 39.36058553293942, 159.399370744574, 717.9907764703582, 217.17666780889454, 349.4475076539325, 325.65893970360105, 85.387514763099, 160.4320538960488, 775.0390878890674, 170.25458434334564, 767.0878969563006, 356.21446215699945, 132.68424011995447, 283.7978305761187, 243.41700668933362, 255.49359306524678, 309.9635633747467, 496.26507277935514, 503.1092159974212, 610.4003017653395, 174.63448202225015, 659.493922949478, 429.3838942954839, 634.8423985761715, 202.3447546395746, 130.23940187983877, 556.2062127949038, 272.7919633961316, 654.6008600346797, 97.86152896990797, 136.7510301620505, 79.07588963519557, 421.2636931002978, 664.5870768004934, 189.95153800968413, 609.7331753481267, 758.3294532172665, 821.039224029989, 893.4133090973293, 215.8074474883401, 134.21868073231684, 605.972012977023, 886.8863578030273, 60.90315198151535],
                [5.436839324817474, -0.4928753183023452, 1.4286927663862068, -1.5130007520377875, 0.16496053834478744, 4.395612412370791, 4.284144375594624, 2.1748747632638934, -1.1934290599645245, 3.4247527120190187, 5.337475505224945, 1.65058699312292, -2.339040851741945, 5.699387796279293, -1.8552582885955595, 1.5264735236448188, 5.914244865973249, 5.3345022969325555, 1.4585125698764108, -0.3517508101394783, 3.251507487187819, 5.055247290549223, -0.5552821455056255, 4.232489994261198, -0.9840277925519643, 0.8739562447750784, 4.745225463816407, -0.24556165743136749, -1.2715326587294213, 0.7986391658629391, -1.917591699063998, -0.5537334054046509, 0.7740718930090648, 2.789767421918547, 1.1038271288908188, 0.7868038361340648, -0.837752119070606, 6.867453056849291, 4.381660254297594, 2.291417949481972, 1.3553749077556951, 0.7529724883224274, -0.02422221247278461, 0.039406296545529185, -1.8755363865799741, 2.039220942575979, 0.9422609887072506, -1.2953827611291664, 0.7704478032444092, 2.079445249853123, 2.5533867503465206, 2.000966153693604, 0.5636644001101144, 1.142952878956058, 1.5686088660949207, 7.666757281561388, 3.4313367608125973, 4.893841287880259, 3.2879425947690923, 2.7168278440045075, 2.3007953346200654, -0.8075840558580839, 3.8456309132028577, 0.8042738197757735, 3.421476396407447, 3.137828975333859, 5.442153271254692, -0.5728561504985411, 3.1609076312729667, 0.8669068510828963, 2.12442695537755, 2.0009735978939385, -0.9260744759065626, 6.3944982356801345, 3.851185025250258, 5.041027383967192, 0.8660247139369208, 2.4019764450608854, 2.546802721479987, 0.3215740354275468, -0.06730543706460368, 4.51681680719285, 3.3689321761858775, -1.6496613361684138, 6.13621755915579, -0.4052894400413017, 2.059903051344407, 2.822356309557156, 2.2265335216450732, 0.004030476219983592, -0.42886520242152204, 4.467940832642515, 4.371327932476514, 4.327196900737048, 5.045300500231654, 1.7861627481092932, 1.233821099748439, 5.1467179970609225, -0.28251733580186666, 3.6216615479991354, 2.7122851070587206, 3.149035166539546, 1.0535551177690679, 1.5830919861483885, 4.658608861359623, 2.343188032831064, -1.613936550937731, 3.3535564342049957, 6.084178891330879, 5.629709189934113, -0.8938389364091149, -0.7217882005662103, -0.43242201040933564, 1.010985165227769, 1.8838002947784007, 4.09806572630087, -2.2399424897034477, 1.0689144193828795, 5.528292273013123, 2.451128333903535, -1.7461923162618826, 3.745466078486035, -0.4880893474940927, -0.6169460086816878, 0.24823857700793694, 2.978971008259412, -0.917688317320605, 3.840631455468187, 3.6518076353035522, -0.9641927360151319, 4.263880693850976, -0.8204638451730356, 1.947003319279932, 0.812307132659795, 0.7090410568417802, 1.0224519085099733, -1.1004510845476967, 3.185769301774804, 1.558889691133881, 2.901852441388067, -0.8536553947172887, 0.12647349810345693, -1.0797565889897933, 1.2438965790277232, 0.24803949359135988, 0.8826523876249466, -1.2880671040521414, 4.451416447619637, 5.1441243003537815, -1.1953254727092233, -1.952861435091085, 2.4179157987528095, 3.841917532157873, 1.6659402369026894, 0.17644046328935636, -1.1875594070282403, -0.3147094712426044, -0.020469564888001113, 3.1796233121315773, 7.458080065934788, -0.19556269450112307, 4.806720335825154, -1.094147581316898, 1.8703743957743286, 1.6684788701478959, 2.256727595560421, 1.8202463624664258, 3.7860946810974583, 0.5828005475103477, -2.4136910901190873, 1.1152051432137677, 6.489027246260084, 6.038695810084724, 1.164299007847514, 3.6867457247376283, 3.774269024463807, 2.023173126725413, 2.090037391379406, 0.5358437460541765, -1.3879054270403643, 4.323517915910993, 1.7431522931853, 1.982850337679004, -0.4133264625742652, 4.6336475802005, -2.120256878017432, 0.7003939587345241, 1.8008653192008197, -0.4688788682373977, 3.2841061984275557, 6.499223815705781, -1.241058102744875, 3.946891042558061, 1.0842827489517088, 2.1194810388506857, -0.03705714048325251, 4.00797782701153, 3.5033527061842165, 4.381267090859683, 0.44269095425477273]]
        ydoe = [list(item) for item in zip(ydoe[0], ydoe[1])]

        hsic = self.analyser.compute_hsic(xdoe, ydoe, SensitivityAnalysisTypes.HsicThresholding.ZERO, 0.20, 0.)

        np.testing.assert_allclose(hsic.r2, [0.0680324,0.0683437,0.0340282,0.0102625,0.0040782], atol=1e-5, rtol=1e-5)
        np.testing.assert_allclose(hsic.indices, [0.00141214,0.00141847,0.000706194,0.000212957,8.46044e-05], atol=1e-5, rtol=1e-5)
        np.testing.assert_allclose(hsic.pvperm, [0,0,0.00990099,0.306931,0.90099], atol=1e-5, rtol=1e-5)
        np.testing.assert_allclose(hsic.pvas, [0.000331762,0.000508135,0.00166787,0.391596,0.834844], atol=1e-5, rtol=1e-5)

