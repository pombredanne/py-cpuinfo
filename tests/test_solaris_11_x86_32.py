

import unittest
import cpuinfo
import helpers


class DataSource(object):
	bits = '32bit'
	cpu_count = 4
	is_windows = False
	raw_arch_string = 'i86pc'

	@staticmethod
	def has_isainfo():
		return True

	@staticmethod
	def has_kstat():
		return True

	@staticmethod
	def isainfo_vb():
		returncode = 0
		output = '''
64-bit amd64 applications
	ssse3 tscp ahf sse3 sse2 sse fxsr mmx cmov amd_sysc cx8 tsc fpu

'''
		return returncode, output

	@staticmethod
	def kstat_m_cpu_info():
		returncode = 0
		output = '''
module: cpu_info                        instance: 0
name:   cpu_info0                       class:    misc
	brand                           Intel(r) Core(tm) i7 CPU         870  @ 2.93GHz
	cache_id                        0
	chip_id                         0
	clock_MHz                       2931
	clog_id                         0
	core_id                         0
	cpu_type                        i386
	crtime                          20.105018108
	cstates_count                   519253:519254
	cstates_nsec                    3370827137067:327348735595
	current_clock_Hz                2930505167
	current_cstate                  0
	current_pstate                  0
	family                          6
	fpu_type                        i387 compatible
	implementation                  x86 (chipid 0x0 GenuineIntel 106E5 family 6 model 30 step 5 clock 2933 MHz)
	max_ncpu_per_chip               4
	max_ncpu_per_core               1
	max_pwrcap                      0
	model                           30
	ncore_per_chip                  4
	ncpu_per_chip                   4
	pg_id                           1
	pkg_core_id                     0
	pstates_count                   null
	pstates_nsec                    null
	snaptime                        3678.092364544
	socket_type                     Unknown
	state                           on-line
	state_begin                     1435089171
	stepping                        5
	supported_frequencies_Hz        2930505167
	supported_max_cstates           1
	supported_max_pstates           0
	vendor_id                       GenuineIntel



'''
		return returncode, output



class TestSolaris(unittest.TestCase):
	def test_all(self):
		helpers.monkey_patch_data_source(cpuinfo, DataSource)

		info = cpuinfo.get_cpu_info_from_kstat()

		self.assertEqual('GenuineIntel', info['vendor_id'])
		self.assertEqual('', info['hardware'])
		self.assertEqual('Intel(r) Core(tm) i7 CPU         870  @ 2.93GHz', info['brand'])
		self.assertEqual('2.9310 GHz', info['hz_advertised'])
		self.assertEqual('2.9305 GHz', info['hz_actual'])
		self.assertEqual((2931000000, 0), info['hz_advertised_raw'])
		self.assertEqual((2930505167, 0), info['hz_actual_raw'])
		self.assertEqual('X86_32', info['arch'])
		self.assertEqual(32, info['bits'])
		self.assertEqual(4, info['count'])

		self.assertEqual('i86pc', info['raw_arch_string'])

		self.assertEqual(0, info['l2_cache_size'])
		self.assertEqual(0, info['l2_cache_line_size'])
		self.assertEqual(0, info['l2_cache_associativity'])

		self.assertEqual(5, info['stepping'])
		self.assertEqual(30, info['model'])
		self.assertEqual(6, info['family'])
		self.assertEqual(0, info['processor_type'])
		self.assertEqual(0, info['extended_model'])
		self.assertEqual(0, info['extended_family'])
		self.assertEqual(
			['ahf', 'amd_sysc', 'cmov', 'cx8', 'fpu', 'fxsr', 'mmx', 'sse', 'sse2', 'sse3', 'ssse3', 'tsc', 'tscp']
			,
			info['flags']
		)
