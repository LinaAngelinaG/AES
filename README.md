# AES
 
 Рабочие файлы разделены следующей логикой:
 - block_cypher содержит реализацию "коробочек" для режимов encryption и decryption
 - encryption содержат алгоритмы шифрования для ecb и cbc
 - decryption содержат алгоритмы дешифрования для ecb и cbc
 - inv_s_box и s_box - содержат матрицы для выполнения преобразования s-box и inv-s-box
 
 #ECB
  запустить в этом режиме шифрования можно следующим способом:
    python main.py [DEC/ENC] [FILENAME] [MODE] [KEY]
    
    DEC/ENC    - флаг, по умолчанию оба имеют значение 'False'
    FILENAME   - имя файла, из которого берется строка hex формата для выполнения операции
    MODE       - метод шифрования - ecb по умолчанию - опционально можно установить и в значение cbc
    KEY        - ключ в hex формате
    
    ##Пример::
    
    
    - для дешифрования
    
    python main.py --dec=True --filename=in2.txt --mode=ecb --key=dc1456e060
    
    - для шифрования
    
    python main.py --enc=True --filename=in.txt --mode=ecb --key=dc1456e060
