import os

def cls(): # очистка экрана
    os.system('cls' if os.name=='nt' else 'clear')

class Hex:
	def __init__(self, hex_value):
		self.hex_value = hex_value

	def getValue(self): # геттер значения переменной
		return self.hex_value

	def _in_bin(self, raw_hex): # перевод в двоичное число (в виде строки)
		raw_bin = format(int(raw_hex, 16),'b')
		if ((len(raw_bin) / 8) != 0):
			for i in range(8 -len(raw_bin)):
				raw_bin = '0' + raw_bin
		return raw_bin

	def _in_hex(self, raw_bin): # перевод в шестнадцатиричное число (в виде строки)
		raw_hex = format(int(raw_bin, 2),'x')
		if (len(raw_hex) == 1):
			raw_hex = '0' + raw_hex
		return raw_hex

	def _XOR(self, value1, value2): # Сложение по модулю 2 между последовательностями бит
		if (len(value1) == 8):
			bin1 = value1
			bin2 = value2
		else:
			bin1 = self._in_bin(value1)
			bin2 = self._in_bin(value2)
		bin_result = ''
		for i in range(len(bin1)):
			bin_result += str(int(bin1[i]) ^ int(bin2[i]))
		hex_result = self._in_hex(bin_result)
		return hex_result

	def __Galois_multiply(self, hex_value, multiplier):# умножение в поле Галуа
		bin_value = self._in_bin(hex_value)
		bin_multiplier = self._in_bin(multiplier)
		result = '00000000'
		cache_result = bin_value
		for i in range(1, 8):
			if (bin_multiplier[7 - i] == '1'):
				cache_result = bin_value
				for j in range(i): 
					cache_result = self.__mult_by_02(cache_result)
				result = self._in_bin(self._XOR(result, cache_result))
		if (bin_multiplier[-1] == '1'):
			result = self._in_bin(self._XOR(result, bin_value))
		return self._in_hex(result)

	def __mult_by_02(self, value): # умножение на {02}
		if (value[0] == '0'):
			value = value + '0'
			value = list(value)
			value.pop(0)
			value = ''.join(value)
		else:
			value = value + '0'
			value = self._XOR(self._in_hex(value), '11b') # 11b - 16-тиричное представление порождающего многочлена
			value = self._in_bin(value)
		return value

	def __add__(self, other): # перегрузка оператора сложения
		XOR_result = self._XOR(self.hex_value, other.getValue())
		return Hex(XOR_result)

	def __mul__(self, other): # перегрузка оператора умножения
		mult_result = self.__Galois_multiply(self.hex_value, other.getValue())
		return Hex(mult_result)


class Coder(Hex):# Работа со строками, шестнадцатиричными числами. Перевод из строки в матрицу и обратно
	def __init__(self):
		self.char_capacity = 8
		self.array_len = 16
		self.matrix_side_size = 4

	def __char_in_bin(self, char): # кодирование одного символа последовательностью бит
		bin_char = format(ord(char), 'b')
		miss_zeros = self.char_capacity - len(bin_char)
		if (miss_zeros != 0):
			for elem in range(miss_zeros):
				bin_char = '0' + bin_char
		return bin_char

	def from_string_in_matrix(self, string):# перевод из строки в матрицу
		if ((len(string) % self.array_len) != 0):
			for i in range(self.array_len - (len(string) % self.array_len)):
				string = string + 'X'
		string_list = [str(item) for item in ''.join(string)]
		matrix = [[0 for j in range(self.matrix_side_size)] for i in range(self.matrix_side_size)]# первый индекс - строка; второй - столбец
		for i in range(4):
			for j in range(4):
				matrix[j][i] = Hex(self._in_hex(self.__char_in_bin(string_list[0])))
				string_list.pop(0)
		return matrix

	def from_matrix_in_string(self, matrix): # перевод из матрицы в строку
		string = ''
		for i in range(self.matrix_side_size):
			for j in range(self.matrix_side_size):
				string = string + chr(int(matrix[j][i].getValue(), 16))
		return string

	def split(self, string): # разбиение строки несколько по 16 в каждой
		if((len(string) % self.array_len) != 0):
			for elem in range(self.array_len - (len(string) % self.array_len)):
				string = string + 'X'
		string = list(string)
		source_arr = []
		for x in range(len(string) // self.array_len):
			cache_arr = []
			for y in range(self.array_len):
				cache_arr.append(string.pop(0))
			cache_arr = ''.join(cache_arr)
			source_arr.append(cache_arr)
		return source_arr


class AES:
	def __init__(self, cipher_key):
		self.SBox =[['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
					['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'], 
					['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'], 
					['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
					['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
					['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39' ,'4a', '4c', '58', 'cf'],
					['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'], 
					['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'], 
					['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'], 
					['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b' ,'db'], 
					['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'], 
					['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'], 
					['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'], 
					['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'], 
					['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'], 
					['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]
		
		self.InvSBox = [['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb'],
						['7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb'],
						['54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e'],
						['08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25'],
						['72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92'],
						['6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84'],
						['90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06'],
						['d0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b'],
						['3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73'],
						['96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e'],
						['47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b'],
						['fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4'],
						['1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f'],
						['60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef'],
						['a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61'],
						['17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']]

		self.mix_cols_matr = [
									[Hex('02'),Hex('03'),Hex('01'),Hex('01')],
									[Hex('01'),Hex('02'),Hex('03'),Hex('01')],
									[Hex('01'),Hex('01'),Hex('02'),Hex('03')],
									[Hex('03'),Hex('01'),Hex('01'),Hex('02')]
									]

		self.inv_mix_cols_matr = [
									[Hex('0e'),Hex('0b'),Hex('0d'),Hex('09')],
									[Hex('09'),Hex('0e'),Hex('0b'),Hex('0d')],
									[Hex('0d'),Hex('09'),Hex('0e'),Hex('0b')],
									[Hex('0b'),Hex('0d'),Hex('09'),Hex('0e')]
									]


		self.matrix_side_size = 4
		self.Rcon = self.__Rcon_form()
		self.Code = Coder()
		self.cipher_key_matrix = self.Code.from_string_in_matrix(cipher_key)
		self.round_key_matriсes = self.__key_schedule()
		self.interface()

	def __Rcon_form(self): # Генерация матрицы Rcon
		matrix = [[0 for j in range(10)] for i in range(4)]# первый индекс - строка; второй - столбец.
		for i in range(10):
			for j in range(1, 4):
				matrix[j][i] = Hex('00')
		top_line = [Hex('01'),Hex('02'),Hex('04'),Hex('08'),Hex('10'),Hex('20'),Hex('40'),Hex('80'),Hex('1b'),Hex('36')] 
		for i in range(10):
			matrix[0][i] = top_line[i]
		return matrix

	def __key_schedule(self): # расширение ключа
		key_matrix_arr =[self.cipher_key_matrix]
		for i in range(len(self.Rcon[0])):
			round_key_matrix = [[0 for m in range(self.matrix_side_size)] for n in range(self.matrix_side_size)]
			last_col = []
			for j in range(self.matrix_side_size):
				last_col.append(key_matrix_arr[-1][j][-1])
			shifted_col = self.__offset(last_col,'up', 1)

			for k in range(len(shifted_col)):
				value = shifted_col[k].getValue()
				shifted_col[k] = Hex(self.SBox[int(value[0], 16)][int(value[1], 16)])
			for l in range(len(shifted_col)):
				round_key_matrix[l][0] = key_matrix_arr[i][l][0] + shifted_col[l] + self.Rcon[l][i]
			for a in range(1, 4):
				for b in range(0, 4):
					round_key_matrix[b][a] = key_matrix_arr[i][b][a] + round_key_matrix[b][a - 1]
			key_matrix_arr.append(round_key_matrix)
		return key_matrix_arr

	def __offset(self, matrix, direction, step_value, num = None): # сдвиг в матрице/векторе заданной строки/столбца в нужном направлении
		if (num != None):
			if (direction == 'up'):
				for s in range(step_value):
					cache = matrix[0][num]
					for i in range(3):
						matrix[i][num] = matrix[i + 1][num]
					matrix[3][num] = cache
			elif (direction == 'right'):
				for i in range(step_value):
					cache = matrix[num][3]
					for i in range(3, 0, -1):
						matrix[num][i] = matrix[num][i - 1]
					matrix[num][0] = cache
			elif (direction == 'down'):
				for i in range(step_value):
					cache = matrix[3][num]
					for i in range(3, 0, -1):
						matrix[i][num] = matrix[i - 1][num]
					matrix[0][num] = cache
			elif (direction == 'left'):
				for i in range(step_value):
					cache = matrix[num][0]
					for i in range(3):
						matrix[num][i] = matrix[num][i + 1]
					matrix[num][3] = cache
			return matrix
		else:
			vector = matrix
			if (direction == 'up'):
				for s in range(step_value):
					cache = vector[0]
					for i in range(3):
						vector[i] = vector[i + 1]
					vector[3] = cache
			elif (direction == 'down'):
				for s in range(step_value):
					cache = vector[3]
					for i in range(3, 0, -1):
						vector[i] = vector[i - 1]
					vector[0] = cache		
			return vector
	
	def sub_bytes(self, matrix, Box): # операция SubBytes
		for i in range(self.matrix_side_size):
			for j in range(self.matrix_side_size):
				value = matrix[i][j].getValue() 
				matrix[i][j] = Hex(Box[int(value[0], 16)][int(value[1], 16)])
		return matrix 

	def shift_rows(self, matrix, direction): # операция ShiftRows
		matrix = self.__offset(matrix, direction, 1, 1)
		matrix = self.__offset(matrix, direction, 2, 2)
		matrix = self.__offset(matrix, direction, 3, 3)
		return matrix

	def mix_columns(self, matrix, mix_cols_matr): # операция MixColumns
		result = [[0 for m in range(self.matrix_side_size)] for n in range(self.matrix_side_size)]
		for i in range(self.matrix_side_size):
			for j in range(self.matrix_side_size):
				result[i][j] = (mix_cols_matr[i][0] * matrix[0][j]) + (mix_cols_matr[i][1] * matrix[1][j]) + (mix_cols_matr[i][2] * matrix[2][j]) + (mix_cols_matr[i][3] * matrix[3][j])
		return result

	def add_round_key(self, matrix, round_key): # операция AddRoundKey
		for i in range(self.matrix_side_size):
			for j in range(self.matrix_side_size):
				matrix[i][j] = matrix[i][j] + round_key[i][j]
		return matrix

	def encrypt_matrix(self, matrix): # шифрование одной матрицы

		matrix = self.add_round_key(matrix, self.round_key_matriсes[0])

		for i in range(1, 10):
			matrix = self.sub_bytes(matrix, self.SBox)
			matrix = self.shift_rows(matrix, 'left')
			matrix = self.mix_columns(matrix, self.mix_cols_matr)
			matrix = self.add_round_key(matrix, self.round_key_matriсes[i])

		matrix = self.sub_bytes(matrix, self.SBox)
		matrix = self.shift_rows(matrix, 'left')
		matrix = self.add_round_key(matrix, self.round_key_matriсes[10])
		return matrix


	def decrypt_matrix(self, matrix): # дешифрование одной матрицы
		matrix = self.add_round_key(matrix, self.round_key_matriсes[0])

		for i in range(1, 10):
			matrix = self.shift_rows(matrix, 'right')
			matrix = self.sub_bytes(matrix, self.InvSBox)
			matrix = self.add_round_key(matrix, self.round_key_matriсes[i])
			matrix = self.mix_columns(matrix, self.inv_mix_cols_matr)
			
		matrix = self.shift_rows(matrix, 'right')
		matrix = self.sub_bytes(matrix, self.InvSBox)
		matrix = self.add_round_key(matrix, self.round_key_matriсes[10])
		return matrix

	def show_matrices(self, matrices, header): # вывод информации в терминал
		for i in range(len(matrices)):
			print(header, i,	':')
			for j in range(4):
				print(matrices[i][j][0].getValue(), matrices[i][j][1].getValue(), matrices[i][j][2].getValue(), matrices[i][j][3].getValue())
			print('')

	def interface(self): # скрипт программы
		message = input('Введите сообщение:')
		splited_message = self.Code.split(message)
		source_matrices = []
		crypted_matrices = []
		decrypted_matrices = []

		#преобразование входящего текста в массив матриц
		for i in range(len(splited_message)):
			source_matrices.append(self.Code.from_string_in_matrix(splited_message[i]))

		self.show_matrices(source_matrices, 'Исходная матрица №')

		#шифрование сообщения
		for i in range(len(splited_message)):
			crypted_matrices.append(self.encrypt_matrix(source_matrices[i]))

		# преобразование зашифрованного сообщения в строку
		crypted_message = ''
		for i in range(len(crypted_matrices)):
			crypted_message = crypted_message + self.Code.from_matrix_in_string(crypted_matrices[i])
		print('Зашифрованное сообщение:', crypted_message)
		print('')

		self.show_matrices(crypted_matrices, 'Зашифрованная матрица №')
		
		# меняю порядок ключей на обратный
		self.round_key_matriсes.reverse()
		
		# дешифрование
		for i in range(len(crypted_matrices)):
			decrypted_matrices.append(self.decrypt_matrix(crypted_matrices[i]))

		self.show_matrices(decrypted_matrices, 'Дешифрованная матрица №')
		
		# преобразование дешифрованного сообщения в строку
		decrypted_message = ''
		for i in range(len(decrypted_matrices)):
			decrypted_message = decrypted_message + self.Code.from_matrix_in_string(decrypted_matrices[i])
		print('Расшифрованное сообщение:', decrypted_message)



AESInst = AES(input('Введите ключевое слово:'))







