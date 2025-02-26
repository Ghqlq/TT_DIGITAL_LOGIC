# # SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# # SPDX-License-Identifier: Apache-2.0

# import cocotb
# from cocotb.clock import Clock
# from cocotb.triggers import ClockCycles


# @cocotb.test()
# async def test_project(dut):
#     dut._log.info("Start")

#     # Set the clock period to 10 us (100 KHz)
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Reset
#     dut._log.info("Reset")
#     dut.ena.value = 1
#     dut.ui_in.value = 0
#     dut.uio_in.value = 0
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     dut._log.info("Test project behavior")

#     # Set the input values you want to test
#     dut.ui_in.value = 20
#     dut.uio_in.value = 30

#     # Wait for one clock cycle to see the output values
#     await ClockCycles(dut.clk, 1)

#     # The following assersion is just an example of how to check the output values.
#     # Change it to match the actual expected output of your module:
#     assert dut.uo_out.value == 50

#     # Keep testing the module by changing the input values, waiting for
#     # one or more clock cycles, and asserting the expected output values.
#         # Test all combinations of ui_in and uio_in across 256 possible values
#     max_val = 255  # Maximum sum value allowed
#     a_vals = [i for i in range(max_val)]  # ui_in can range from 0 to 255
#     b_vals = [j for j in range(max_val)]  # uio_in can also range from 0 to 255

#     for i in range(len(a_vals)):
#         for j in range(len(b_vals)):
#             # Set the input values
#             dut.ui_in.value = a_vals[i]
#             dut.uio_in.value = b_vals[j]

#             # Wait for one or more clock cycles to see the output values
#             await ClockCycles(dut.clk, 20)  # Allow enough time for the DUT to process

#             # Log the output and check the assertion
#             dut._log.info(f"Test case ui_in={a_vals[i]}, uio_in={b_vals[j]} -> uo_out={dut.uo_out.value}")

#             # Expected output logic (assuming sum modulo 256, replace as per DUT logic)
#             expected_uo_out = (a_vals[i] + b_vals[j]) % 256

#             # Assert the output matches the expected value
#             assert int(dut.uo_out.value) == expected_uo_out, (
#                 f"Test failed for ui_in={a_vals[i]}, uio_in={b_vals[j]}. Expected {expected_uo_out}, "
#                 f"but got {dut.uo_out.value}")
            
#             # Optionally log the test case result if the assertion passed
#             dut._log.info(f"Test passed for ui_in={a_vals[i]}, uio_in={b_vals[j]} with uo_out={dut.uo_out.value}")

import cocotb
from cocotb.triggers import Timer

# Clock generator coroutine
async def clock_gen(dut):
    while True:
        dut.clk.value = 0
        await Timer(5, units="ns")
        dut.clk.value = 1
        await Timer(5, units="ns")

@cocotb.test()
async def test_priority_encoder(dut):
    dut._log.info("Starting priority encoder test")

    # Reset sequence
    dut.rst_n.value = 0
    await Timer(10, units="ns")
    dut.rst_n.value = 1

    # Start the clock process
    cocotb.start_soon(clock_gen(dut))

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    test_cases = [
        (0b10000000, 0b00000000, 15),
        (0b01000000, 0b00000000, 14),
        (0b00100000, 0b00000000, 13),
        (0b00010000, 0b00000000, 12),
        (0b00001000, 0b00000000, 11),
        (0b00000100, 0b00000000, 10),
        (0b00000010, 0b00000000, 9),
        (0b00000001, 0b00000000, 8),
        (0b00000000, 0b10000000, 7),
        (0b00000000, 0b01000000, 6),
        (0b00000000, 0b00100000, 5),
        (0b00000000, 0b00010000, 4),
        (0b00000000, 0b00001000, 3),
        (0b00000000, 0b00000100, 2),
        (0b00000000, 0b00000010, 1),
        (0b00000000, 0b00000001, 0),
        (0b00000000, 0b00000000, 0b11110000), # No bits set case
    ]

    for ui, uio, expected in test_cases:
        dut.ui_in.value = ui
        dut.uio_in.value = uio
        await Timer(10, units="ns")
        actual = int(dut.uo_out.value)
        dut._log.info(f"ui_in: {bin(ui)}, uio_in: {bin(uio)}, Expected: {expected}, Got: {actual}")
        assert actual == expected, f"Expected {expected}, got {actual}"

