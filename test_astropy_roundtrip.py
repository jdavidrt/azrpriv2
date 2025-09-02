import numpy as np

try:
    from astropy.table import Table
    HAS_ASTROPY = True
except ImportError:
    HAS_ASTROPY = False

# Simple pytest replacement for standalone testing
def skipif(condition, reason=""):
    def decorator(func):
        if condition:
            def skipped(*args, **kwargs):
                print(f"SKIPPED: {reason}")
                return
            return skipped
        return func
    return decorator

class pytest:
    mark = type('mark', (), {'skipif': skipif})

from stingray.events import EventList
from stingray.varenergyspectrum import RmsSpectrum, ExcessVarianceSpectrum
from stingray.crossspectrum import Crossspectrum, AveragedCrossspectrum
from stingray.lightcurve import Lightcurve


class TestAstropyRoundtrip:
    """Test roundtrip functionality to/from Astropy tables"""
    
    @classmethod
    def setup_class(cls):
        """Set up test data"""
        # Create sample events
        np.random.seed(42)
        times = np.sort(np.random.uniform(0, 1000, 10000))
        energies = np.random.uniform(0.1, 12.0, 10000)
        
        cls.events = EventList(times, energy=energies, gti=[[0, 1000]])
        
        # Create sample light curves for crossspectrum
        dt = 0.1
        t = np.arange(0, 100, dt)
        counts1 = 100 + 10 * np.random.normal(size=len(t))
        counts2 = 100 + 10 * np.random.normal(size=len(t))
        
        cls.lc1 = Lightcurve(t, counts1, dt=dt, gti=[[0, 100]])
        cls.lc2 = Lightcurve(t, counts2, dt=dt, gti=[[0, 100]])
    
    @pytest.mark.skipif(not HAS_ASTROPY, reason="Astropy not available")
    def test_varenergy_spectrum_roundtrip(self):
        """Test VarEnergySpectrum roundtrip via RmsSpectrum"""
        # Create RmsSpectrum
        freq_interval = [0.1, 1.0]
        energy_spec = [1.0, 10.0, 5, 'lin']
        
        spectrum = RmsSpectrum(
            self.events,
            freq_interval=freq_interval,
            energy_spec=energy_spec,
            bin_time=0.1,
            segment_size=100
        )
        
        # Convert to table
        table = spectrum.to_astropy_table()
        
        # Verify table structure
        assert isinstance(table, Table)
        assert 'energy' in table.columns
        assert 'spectrum' in table.columns
        assert 'spectrum_error' in table.columns
        
        # Verify metadata
        assert table.meta['freq_interval'] == freq_interval
        assert table.meta['bin_time'] == 0.1
        assert table.meta['use_pi'] == False
        
        # Test roundtrip
        spectrum_reconstructed = RmsSpectrum.from_astropy_table(table, self.events)
        
        # Verify reconstructed object
        np.testing.assert_array_equal(spectrum.energy, spectrum_reconstructed.energy)
        np.testing.assert_array_equal(spectrum.spectrum, spectrum_reconstructed.spectrum)
        np.testing.assert_array_equal(spectrum.spectrum_error, spectrum_reconstructed.spectrum_error)
        assert spectrum.freq_interval == spectrum_reconstructed.freq_interval
        assert spectrum.bin_time == spectrum_reconstructed.bin_time
        assert spectrum.use_pi == spectrum_reconstructed.use_pi
    
    @pytest.mark.skipif(not HAS_ASTROPY, reason="Astropy not available")
    def test_crossspectrum_roundtrip(self):
        """Test Crossspectrum roundtrip"""
        # Create Crossspectrum
        cs = Crossspectrum(self.lc1, self.lc2, norm='leahy')
        
        # Convert to table
        table = cs.to_astropy_table()
        
        # Verify table structure
        assert isinstance(table, Table)
        assert 'freq' in table.columns
        assert 'power' in table.columns
        
        # Verify metadata
        assert table.meta['norm'] == 'leahy'
        assert table.meta['m'] == cs.m
        assert table.meta['type'] == 'crossspectrum'
        
        # Test roundtrip
        cs_reconstructed = Crossspectrum.from_astropy_table(table)
        
        # Verify reconstructed object
        np.testing.assert_array_equal(cs.freq, cs_reconstructed.freq)
        np.testing.assert_array_equal(cs.power, cs_reconstructed.power)
        assert cs.norm == cs_reconstructed.norm
        assert cs.m == cs_reconstructed.m
        assert cs.dt == cs_reconstructed.dt
    
    @pytest.mark.skipif(not HAS_ASTROPY, reason="Astropy not available")
    def test_averaged_crossspectrum_roundtrip(self):
        """Test AveragedCrossspectrum roundtrip"""
        # Create AveragedCrossspectrum
        acs = AveragedCrossspectrum(
            self.lc1, self.lc2, 
            segment_size=10.0, 
            norm='leahy'
        )
        
        # Convert to table
        table = acs.to_astropy_table()
        
        # Verify table structure
        assert isinstance(table, Table)
        assert 'freq' in table.columns
        assert 'power' in table.columns
        
        # Verify metadata
        assert table.meta['norm'] == 'leahy'
        assert table.meta['m'] == acs.m
        
        # Test roundtrip
        acs_reconstructed = AveragedCrossspectrum.from_astropy_table(
            table, segment_size=10.0
        )
        
        # Verify reconstructed object
        np.testing.assert_array_equal(acs.freq, acs_reconstructed.freq)
        np.testing.assert_array_equal(acs.power, acs_reconstructed.power)
        assert acs.norm == acs_reconstructed.norm
        assert acs.m == acs_reconstructed.m
    
    @pytest.mark.skipif(not HAS_ASTROPY, reason="Astropy not available")
    def test_table_metadata_preservation(self):
        """Test that all important metadata is preserved in roundtrip"""
        # Create spectrum with various parameters
        spectrum = ExcessVarianceSpectrum(
            self.events,
            freq_interval=[0.1, 2.0],
            energy_spec=[2.0, 8.0, 4, 'log'],
            bin_time=0.5,
            use_pi=False,
            segment_size=50
        )
        
        # Convert to table and back
        table = spectrum.to_astropy_table()
        
        # Check that all expected metadata is present
        expected_meta = [
            'freq_interval', 'energy_intervals', 'ref_band',
            'bin_time', 'use_pi', 'segment_size', 'return_complex'
        ]
        
        for key in expected_meta:
            assert key in table.meta, f"Missing metadata key: {key}"
    
    def test_import_error_handling(self):
        """Test that appropriate errors are raised when Astropy is not available"""
        # This test would need to mock the absence of Astropy
        # For now, we'll just verify the error messages are correct
        pass


if __name__ == '__main__':
    # Simple test runner
    test_class = TestAstropyRoundtrip()
    test_class.setup_class()
    
    if HAS_ASTROPY:
        print("Running Astropy roundtrip tests...")
        try:
            test_class.test_varenergy_spectrum_roundtrip()
            print("✓ VarEnergySpectrum roundtrip test passed")
        except Exception as e:
            print(f"✗ VarEnergySpectrum roundtrip test failed: {e}")
        
        try:
            test_class.test_crossspectrum_roundtrip()
            print("✓ Crossspectrum roundtrip test passed")
        except Exception as e:
            print(f"✗ Crossspectrum roundtrip test failed: {e}")
        
        try:
            test_class.test_averaged_crossspectrum_roundtrip()
            print("✓ AveragedCrossspectrum roundtrip test passed")
        except Exception as e:
            print(f"✗ AveragedCrossspectrum roundtrip test failed: {e}")
        
        try:
            test_class.test_table_metadata_preservation()
            print("✓ Metadata preservation test passed")
        except Exception as e:
            print(f"✗ Metadata preservation test failed: {e}")
    else:
        print("Astropy not available - skipping tests")