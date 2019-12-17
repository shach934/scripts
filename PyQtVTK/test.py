import os
import re
path = """// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [ 0 2 -3 0 0 0 0 ];

internalField   uniform 1;

boundaryField
{
    furnace
    {
        type            epsilonWallFunction;
        value           $internalField;
    }
    tube
    {
        type            epsilonWallFunction;
        value           $internalField;
    }
    rotor
    {
        type            epsilonWallFunction;
        value           $internalField;
    }
    sensor
    {
        type            epsilonWallFunction;
        value           $internalField;
    }
    buffel
    {
        type            epsilonWallFunction;
        value           $internalField;
    }
    rr_slave
    {
        type            cyclicAMI;
        value           $internalField;
    }
    atmosphere
    {
        type            inletOutlet;
        value           $internalField;
        inletValue      $internalField;
    }
    rr
    {
        type            cyclicAMI;
        value           $internalField;
    }
}


// ************************************************************************* //
"""
print(re.findall("omega\s+(\S+)\s+(.*?)\s*;", path))