run_tests:
	python3 main.py -fp dynamic_small_network.txt -a 1 --cds
	python3 main.py -fp dynamic_small_network.txt -a 2 --cds
	python3 main.py -fp dynamic_small_network.txt -a 3 --cds -k 1 -m 1
	python3 main.py -fp dynamic_small_network.txt -a 3 --cds -k 1 -m 2
	python3 main.py -fp dynamic_small_network.txt -a 3 --cds -k 1 -m 3
	python3 main.py -fp dynamic_small_network.txt -a 1 --mcds
	python3 main.py -fp dynamic_small_network.txt -a 2 --mcds		
	python3 main.py -fp dynamic_small_network.txt -a 3 --mcds -k 1 -m 1
	python3 main.py -fp dynamic_small_network.txt -a 3 --mcds -k 1 -m 2
	python3 main.py -fp dynamic_small_network.txt -a 3 --mcds -k 1 -m 3
	python3 main.py -fp dynamic_small_network.txt -a 3 --rmcds -k 1 -m 1
	python3 main.py -fp dynamic_small_network.txt -a 3 --rmcds -k 1 -m 2
	python3 main.py -fp dynamic_small_network.txt -a 3 --rmcds -k 1 -m 3

tests_with_logging:
	python3 main.py -fp dynamic_small_network.txt -a 1 --cds --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 2 --cds --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --cds -k 1 -m 1 --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --cds -k 1 -m 2 --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --cds -k 1 -m 3 --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 1 --mcds --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 2 --mcds --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --mcds -k 1 -m 1 --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --mcds -k 1 -m 2 --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --mcds -k 1 -m 3 --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --rmcds -k 1 -m 1 --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --rmcds -k 1 -m 2 --log -lv debug
	python3 main.py -fp dynamic_small_network.txt -a 3 --rmcds -k 1 -m 3 --log -lv debug
