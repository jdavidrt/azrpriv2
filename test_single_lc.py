#!/usr/bin/env python3

"""
Test script to understand the issue with from_lc_iterable and from_lightcurve
for single light curve processing.
"""

import numpy as np
from stingray import Lightcurve
from stingray.powerspectrum import Powerspectrum, AveragedPowerspectrum
from stingray.crossspectrum import Crossspectrum, AveragedCrossspectrum

def test_single_lightcurve_issue():
    """Test both methods with a single light curve to understand the difference."""
    
    # Create a simple test light curve
    np.random.seed(42)
    time = np.linspace(0, 100, 1000)
    counts = 100 + 10 * np.sin(2 * np.pi * 0.1 * time) + np.random.poisson(5, len(time))
    lc = Lightcurve(time, counts)
    
    print("Testing single light curve processing...")
    print(f"Light curve length: {len(lc.time)}")
    print(f"Light curve dt: {lc.dt}")
    print(f"Light curve duration: {lc.tseg}")
    
    # Test from_lightcurve (should work for single light curve)
    print("\n=== Testing from_lightcurve ===")
    try:
        ps_from_lc = AveragedPowerspectrum.from_lightcurve(lc, segment_size=20)
        print(f"from_lightcurve - Success!")
        print(f"  Number of segments: {ps_from_lc.m}")
        print(f"  Frequency range: {ps_from_lc.freq[0]:.4f} - {ps_from_lc.freq[-1]:.4f}")
        print(f"  Power range: {np.min(ps_from_lc.power):.4f} - {np.max(ps_from_lc.power):.4f}")
    except Exception as e:
        print(f"from_lightcurve - Error: {e}")
    
    # Test from_lc_iterable with single light curve (as a list)
    print("\n=== Testing from_lc_iterable with single light curve ===")
    try:
        ps_from_iter = AveragedPowerspectrum.from_lc_iterable([lc], dt=lc.dt, segment_size=20)
        print(f"from_lc_iterable - Success!")
        print(f"  Number of segments: {ps_from_iter.m}")
        print(f"  Frequency range: {ps_from_iter.freq[0]:.4f} - {ps_from_iter.freq[-1]:.4f}")
        print(f"  Power range: {np.min(ps_from_iter.power):.4f} - {np.max(ps_from_iter.power):.4f}")
    except Exception as e:
        print(f"from_lc_iterable - Error: {e}")
    
    # Compare results if both work
    print("\n=== Comparison ===")
    try:
        if 'ps_from_lc' in locals() and 'ps_from_iter' in locals():
            print(f"Results are equivalent: {np.allclose(ps_from_lc.power, ps_from_iter.power)}")
            if not np.allclose(ps_from_lc.power, ps_from_iter.power):
                print(f"Max difference: {np.max(np.abs(ps_from_lc.power - ps_from_iter.power))}")
        else:
            print("Cannot compare - one or both methods failed")
    except:
        print("Comparison failed")
        
    # Test with no segment_size (single spectrum)
    print("\n=== Testing without segment_size (single spectrum) ===")
    try:
        ps_single_lc = Powerspectrum.from_lightcurve(lc)
        print(f"Single spectrum from_lightcurve - Success!")
        print(f"  Number of points: {len(ps_single_lc.freq)}")
    except Exception as e:
        print(f"Single spectrum from_lightcurve - Error: {e}")
        
    try:
        ps_single_iter = Powerspectrum.from_lc_iterable([lc], dt=lc.dt)
        print(f"Single spectrum from_lc_iterable - Success!")
        print(f"  Number of points: {len(ps_single_iter.freq)}")
    except Exception as e:
        print(f"Single spectrum from_lc_iterable - Error: {e}")

if __name__ == "__main__":
    test_single_lightcurve_issue()