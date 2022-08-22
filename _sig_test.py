import sys
sys.path.append(r'/mnt/extra-addons/pycades_0.1.22769/build')
import pycades
import logging

_logger = logging.getLogger(__name__)


def get_sign(data, KeyPin=None, detached=False):
    # Вид подписи: отделенная (true) или совмещенная (false). По умолчанию совмещенная
    store = pycades.Store()
    _logger.info(f"Пытаюсь получить сертификат УКЭП")
    store.Open(pycades.CADESCOM_CONTAINER_STORE, pycades.CAPICOM_MY_STORE,
               pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED)
    certs = store.Certificates
    print(certs.Count, '- кол-во найденных сертификатов')
    assert (certs.Count != 0), "Certificates with private key not found"

    signer = pycades.Signer()
    cert = certs.Find(pycades.CAPICOM_CERTIFICATE_FIND_SHA1_HASH, 'd6a831405297fcd00efb50557f7ac32cc541f0cf')
    #cert = certs.Find(pycades.CAPICOM_CERTIFICATE_FIND_SHA1_HASH, '5696ef17a824969cd604fa9bee2d81f0c0a1c1d4')
    #cert = certs.Find(pycades.CAPICOM_CERTIFICATE_FIND_SHA1_HASH, 'adc3735718e8bef6a444c6f6a2335195de148be4')
    assert (cert.Count != 0), "Сертификат с заданным HASH '5696ef17a824969cd604fa9bee2d81f0c0a1c1d4' не найден."
    print(cert)
    signer.Certificate = cert.Item(1)

    signer.CheckCertificate = True
    if KeyPin:
        signer.KeyPin = KeyPin

    signedData = pycades.SignedData()
    signedData.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
    signedData.Content = data
    print(f"Начал подпись данных с помощью сертификата {signer.Certificate}")
    signature = signedData.SignCades(signer, pycades.CADESCOM_CADES_BES, detached)
    print(f"Подписал данные")

    if not detached:
        _signedData = pycades.SignedData()
        _signedData.VerifyCades(signature, pycades.CADESCOM_CADES_BES)
        print("Verified successfully")

    return True



sign = get_sign(data='RFVZQlBPUklBV1lCTlpYTElMRlNSTVdCV0hMQUZI')
if sign:
    print('Успех')


