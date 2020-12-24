////////////////////////////////////////////////////////////////////////////////
// The following FIT Protocol software provided may be used with FIT protocol
// devices only and remains the copyrighted property of Garmin Canada Inc.
// The software is being provided on an "as-is" basis and as an accommodation,
// and therefore all warranties, representations, or guarantees of any kind
// (whether express, implied or statutory) including, without limitation,
// warranties of merchantability, non-infringement, or fitness for a particular
// purpose, are specifically disclaimed.
//
// Copyright 2020 Garmin Canada Inc.
////////////////////////////////////////////////////////////////////////////////
// ****WARNING****  This file is auto-generated!  Do NOT edit this file.
// Profile Version = 21.40Release
// Tag = production/akw/21.40.00-0-g813c158
////////////////////////////////////////////////////////////////////////////////


package com.garmin.fit;

public class FieldComponent {
    protected int fieldNum;
    protected boolean accumulate;
    protected int bits;
    protected double scale;
    protected double offset;

    protected FieldComponent(int fieldNum, boolean accumulate, int bits, double scale, double offset) {
        this.fieldNum = fieldNum;
        this.accumulate = accumulate;
        this.bits = bits;
        this.scale = scale;
        this.offset = offset;
    }
}
