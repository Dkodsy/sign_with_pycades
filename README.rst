================================================
Установка PyCades
================================================

.. contents::
   :local:

Инструкции по установке
================================================

Предварительно в '/extra-addons' поместим необходимые файлы для работы с электронной подписью:

* 1. linux-amd64_deb.tgz *(доступно по ссылке - https://cryptopro.ru/sites/default/files/private/csp/50/11455/linux-amd64_deb.tgz)*
* 2. cades_linux_amd64.tar.gz *(доступно по ссылке - https://cryptopro.ru/sites/default/files/products/cades/current_release_2_0/cades_linux_amd64.tar.gz)*
* 3. Архив с исходниками pycades *(доступно по ссылке - https://cryptopro.ru/sites/default/files/products/cades/pycades/pycades.zip)*
* 4. Контейнер УКЭП закрытого типа *(прим. - такого контейнера - te-6ec6c.000).*
* 5. Сертификат который ассоциируется с контейнером *(прим. - certificate.cer).*
* 6. Сертификаты удостоверяющего центра, где получена подпись, список сертификатов можно получить при обращении к УЦ, которая выдавала УКЭП *(прим. - rootca.cer).*

**Установка Крипто Про**


* 1. Входим в контейнер docker под "root":
    * 1. **docker exec -u 0 -it mycontainer bash**

* 2. Обновляем пакеты:
    * 1. **apt update**

* 3. Перейдем в каталог с архивом КриптоПро(linux-amd64_deb.tgz) и установим его:
    * 1.  **сd /mnt/extra-addons**
    * 2.  **tar xvf linux-amd64_deb.tgz**
    * 3.  **cd linux-amd64_deb**
    * 4.  **./install.sh**

* 4. Установим пакет cprocsp-devel из этой же дирректории:
    * 1. **apt install ./lsb-cprocsp-devel_5.0*.deb**

* 5. Установка завершена, делаем симлинки:
    * 1.  **cd /bin**
    * 2.  **ln -s /opt/cprocsp/bin/amd64/certmgr**
    * 3.  **ln -s /opt/cprocsp/bin/amd64/cpverify**
    * 4.  **ln -s /opt/cprocsp/bin/amd64/cryptcp**
    * 5.  **ln -s /opt/cprocsp/bin/amd64/csptest**
    * 6.  **ln -s /opt/cprocsp/bin/amd64/csptestf**
    * 7.  **ln -s /opt/cprocsp/sbin/amd64/cpconfig**

----

**Установка КриптоПро ЭЦП SDK**

* 1. Вернемся в директорию с необходимыми файлами:
    * 1. **cd /mnt/extra-addons**
* 2. Распакуем архив(cades_linux_amd64.tar.gz) и установим пакет cprocsp-pki-cades:
    * 1.  tar xvf cades_linux_amd64.tar.gz
    * 2.  cd cades_linux_amd64
    * 3.  apt install ./cprocsp-pki-cades*.deb

----

**Установка расширения pycades**

* 1. Обновляем пакеты:
    * 1. **apt update**

* 2. Устанавливаем необходимые компоненты для установки и работы библиотеки pycades:
    * 1.  **apt install cmake build-essential libboost-all-dev python3-dev unzip nano**

* 3. Вернемся в дирректорию с архивом pycades и распакуем его:
    * 1.  cd /mnt/extra-addons
    * 2.  unzip pycades.zip
    * 3.  cd pycades_*

* 4. Задаем значение переменной Python_INCLUDE_DIR в файле CMakeLists.txt:
    * 1.  find / -iname 'Python.h' *- находим папку с Python.h*
    * 2.  Получаем путь до дирректории с файлом Python.h *- /usr/include/python3.7m/Python.h*
    * 3.  Указываем данный путь в формате "/usr/include/python3.7" в файле CMakeLists.txt:
            * 1. nano CMakeLists.txt
            * 2. Указываем во второй строке путь  - * пример - SET(Python_INCLUDE_DIR "/usr/include/python3.7")*
            * 3. ctrl-X ==> Y ==> enter

* 5. Выполняем сборку библиотеки pycades:
    * 1.  mkdir build
    * 2.  cd build
    * 3.  cmake ..
    * 4.  make -j4

* 6. Экспортируем путь до собранной библиотеки в системную переменную PYTHONPATH:
    * 1. echo 'export PYTHONPATH=/path_to_pycades_so' >> ~/.bashrc    **(пример /path_to_pycades_os/ ----- /mnt/extra-addons/pycades_0.1.22769/build/)**
    * 2. source ~/.bashrc

**Примечание**
* 1. При сборке библиотеки возможна ошибка - "fatal error: asn1/Attribute.h: Нет такого файла или каталога", решение:
    * 1. cd /mnt/extra-addons
    * 2. wget https://www.cryptopro.ru/sites/default/files/public/faq/csp/csp5devel.tgz
    * 3. tar xvf csp5devel.tgz
    * 4. cd csp5devel
    * 5. apt install ./lsb-cprocsp-devel_5.0.11863-5_all.deb
    * 6. Вернуться в папку build *(прим. cd /mnt/extra-addons/pycades_0.1.22769/build/)*
    * 7. Вернуться к сборке библиотеки pycades


----

**Установка УКЭП**

* 1. Скопировать ключ в хранилище(контейнер Криптопро):
    * 1. cp -R /mnt/extra-addons/*te-6ec6c.000*/ /var/opt/cprocsp/keys/*odoo*/

* 2. Поставить необходимые права, как того требует КриптоПро:
    * 1. chown -R odoo /var/opt/cprocsp/keys/odoo
    * 2. chmod 600 /var/opt/cprocsp/keys/odoo

* 3. Войдем в docker под odoo юзером:
    * 1. exit
    * 2. sudo docker exec -it odoo bash

* 4. Узнаем настоящее название контейнера:
    * 1. csptest -keyset -enum_cont -verifycontext -fqcn
    * 2. Пример ответа *AcquireContext: OK. HCRYPTPROV: 41074515 \\\\.\\HDIMAGE\\te-6ec6ce49-f8d5-4220-875b-fd262f7e5014 OK.Total: SYS: 0,010 sec USR: 0,070 sec UTC: 0,090 sec[ErrorCode: 0x00000000]*, где **"\\\\.\\HDIMAGE\\te-6ec6ce49-f8d5-4220-875b-fd262f7e5014"** - имя контейнера

* 5. Ассоциировать сертификат с контейнером, сертификат попадет в пользовательское хранилище My:
    * 1. certmgr -inst -file /mnt/extra-addons/certificate.cer -cont '\\\\.\\HDIMAGE\\te-6ec6ce49-f8d5-4220-875b-fd262f7e5014'
    * 2. Если следующая ошибка, нужно узнать реальное название контейнера (см. выше): *Failed to open container \\\\.\\HDIMAGE\\<container> [ErrorCode: 0x00000002]*

* 6. Установить сертификат УЦ из-под пользователя root командой:
    * 1. certmgr -inst -store uroot -file /mnt/extra-addons/rootca.cer *(путь до сертификата УЦ)*

* 7. Проверка корректности установки сертификата:
    * 1. certmgr --list
    * 2. PrivateKey Link: Yes     Container: HDIMAGE\\\\te-6ec6c.000\\FE30 - *успешная установка сертификата*

**Примечание**
* 1. Для тестового контура можно сгенерировать тестовую УКЭП по инструкции по ссылке:
    * 1. https://track.crpt.ru/sl/8e9744386fd720b62f56dac0945fb6c316/
    * 2. Генерацию тестового ключа по инструкции рекомендуется делать с OC Windows

----
