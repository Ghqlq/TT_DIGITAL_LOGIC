// /*
//  * Copyright (c) 2024 Your Name
//  * SPDX-License-Identifier: Apache-2.0
//  */

// `default_nettype none

// module tt_um_adder_TT10_digitalLogic (
//     input  wire [7:0] ui_in,    // Dedicated inputs
//     output wire [7:0] uo_out,   // Dedicated outputs
//     input  wire [7:0] uio_in,   // IOs: Input path
//     output wire [7:0] uio_out,  // IOs: Output path
//     output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
//     input  wire       ena,      // always 1 when the design is powered, so you can ignore it
//     input  wire       clk,      // clock
//     input  wire       rst_n     // reset_n - low to reset
// );

//   // All output pins must be assigned. If not used, assign to 0.
//   assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
//   assign uio_out = 0;
//   assign uio_oe  = 0;
  

//   // List all unused inputs to prevent warnings
//   wire _unused = &{ena, clk, rst_n, 1'b0};

// endmodule

`default_nettype none

module tt_um_priority_encoder (
    input  wire [7:0] ui_in,    // 8-bit input A
    output wire [7:0] uo_out,   // 8-bit output C
    input  wire [7:0] uio_in,   // 8-bit input B
    output wire [7:0] uio_out,  // Unused, assigned to 0
    output wire [7:0] uio_oe,   // Unused, assigned to 0
    input  wire       ena,      // Always 1 when powered, ignored
    input  wire       clk,      // Clock, not used in combinational logic
    input  wire       rst_n     // Active low reset, ignored
);

    wire [15:0] in_data;  // Combined input signal
    reg [7:0] out_data;   // Output from priority encoder

    // Combine A[7:0] and B[7:0] to form In[15:0]
    assign in_data = {ui_in, uio_in};

    // Priority Encoder Logic using if-else
    always @(*) begin
        if (in_data[15]) out_data = 8'd15;
        else if (in_data[14]) out_data = 8'd14;
        else if (in_data[13]) out_data = 8'd13;
        else if (in_data[12]) out_data = 8'd12;
        else if (in_data[11]) out_data = 8'd11;
        else if (in_data[10]) out_data = 8'd10;
        else if (in_data[9]) out_data = 8'd9;
        else if (in_data[8]) out_data = 8'd8;
        else if (in_data[7]) out_data = 8'd7;
        else if (in_data[6]) out_data = 8'd6;
        else if (in_data[5]) out_data = 8'd5;
        else if (in_data[4]) out_data = 8'd4;
        else if (in_data[3]) out_data = 8'd3;
        else if (in_data[2]) out_data = 8'd2;
        else if (in_data[1]) out_data = 8'd1;
        else if (in_data[0]) out_data = 8'd0;
        else out_data = 8'b11110000; // No '1' found case
    end

    // Assign outputs
    assign uo_out  = out_data;
    assign uio_out = 8'b00000000;
    assign uio_oe  = 8'b00000000;

endmodule
