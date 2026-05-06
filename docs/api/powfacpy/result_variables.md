Module powfacpy.result_variables
================================
This module provides enumeration classes for results variables of 'Elm' classes (network elements). This is convenient to get results variable strings and supports code completion in your IDE. If you hover over a variable, it's unit and description will be shown.  

This file is automatically created using the .txt files in '\.esult_variables' and using the module 'results_varaibles_parser'. The .txt files are created by copying from the output window of PF (manually) using the printed results variables when clicking on 'Variable List' in an .IntMon file of an 'Elm' class.

Currently, the following 'Elm' classes are supported: 

ElmArea
ElmAsm
ElmAsmsc
ElmBoundary
ElmCoup
ElmGenstat
ElmIac
ElmLne
ElmLod
ElmLodlv
ElmLodmv
ElmPvsys
ElmSecctrl
ElmShnt
ElmSind
ElmStactrl
ElmSym
ElmTerm
ElmTr2
ElmTr3
ElmVac
ElmVsc
ElmVscmono
ElmXnet
ElmZone
ElmZpu
StaPll

The follwing simulation types/result variable types are supported:

Basic Data balanced: Basic
Load Flow AC balanced: LF_Bal
Load Flow AC unbalanced: LF_Unbal
Simulation RMS balanced: RMS_Bal
Simulation RMS unbalanced: RMS_Unbal
Simulation EMT unbalanced: EMT
Sensitivities / Distribution Factors AC balanced: Sensitivities_Bal

Classes
-------

`ResVar()`
:   

    ### Class variables

    `Basic`
    :   The type of the None singleton.

    `EMT`
    :   The type of the None singleton.

    `LF_Bal`
    :   The type of the None singleton.

    `LF_Unbal`
    :   The type of the None singleton.

    `RMS_Bal`
    :   The type of the None singleton.

    `RMS_Unbal`
    :   The type of the None singleton.

    `Sensitivities_Bal`
    :   The type of the None singleton.