import sys

sys.path.append(r'/extra-addons/pycades_0.1.22769/build/')
import pycades
import logging

_logger = logging.getLogger(__name__)


def get_sign(data, sha_hash, KeyPin=None, detached=False):
    # Вид подписи: отделенная (true) или совмещенная (false). По умолчанию совмещенная
    store = pycades.Store()
    _logger.info(f"Пытаюсь получить сертификат УКЭП")
    store.Open(pycades.CADESCOM_CONTAINER_STORE, pycades.CAPICOM_MY_STORE,
               pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED)
    certs = store.Certificates
    assert (certs.Count != 0), "Certificates with private key not found"
    signer = pycades.Signer()
    cert = certs.Find(pycades.CAPICOM_CERTIFICATE_FIND_SHA1_HASH, str(sha_hash))
    assert (cert.Count != 0), f"Сертификат с заданным HASH {sha_hash} не найден."
    signer.Certificate = cert.Item(1)

    signer.CheckCertificate = True
    if KeyPin:
        signer.KeyPin = KeyPin

    signedData = pycades.SignedData()
    signedData.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
    signedData.Content = data
    _logger.info(f"Начал подпись данных с помощью сертификата {signer.Certificate}")
    signature = signedData.SignCades(signer, pycades.CADESCOM_CADES_BES, detached)
    _logger.info(f"Подписал данные")

    if not detached:
        _signedData = pycades.SignedData()
        _signedData.VerifyCades(signature, pycades.CADESCOM_CADES_BES)
        _logger.info("Verified successfully")

    return signature


def get_off_sign(KeyPin=None):
    store = pycades.Store()
    store.Open(pycades.CADESCOM_CONTAINER_STORE, pycades.CAPICOM_MY_STORE, pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED)
    certs = store.Certificates
    assert (certs.Count != 0), "Certificates with private key not found"

    signer = pycades.Signer()
    signer.Certificate = certs.Item(1)
    signer.CheckCertificate = True
    if KeyPin:
        signer.KeyPin = KeyPin

    hashedData = pycades.HashedData()
    hashedData.Algorithm = pycades.CADESCOM_HASH_ALGORITHM_CP_GOST_3411_2012_256
    hashedData.Hash("test data")

    signedData = pycades.SignedData()
    signature = signedData.SignHash(hashedData, signer, pycades.CADESCOM_CADES_BES)

    _signedData = pycades.SignedData()
    _signedData.VerifyHash(hashedData, signature, pycades.CADESCOM_CADES_BES)
    return signature