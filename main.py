"""
AUTOMATIC POSITION CALCULATOR VER.3
"""

import sys


import portfolios as pt
import helper
import rebalancing as rb
import backtesting as bt

version = 3

helper.print_header("AUTOMATIC POSITION CALCULATOR - VERSION " + str(version))

# Model Portfolios List

balanced = {'VFV.TO': 0.5, 'XBB.TO': 0.5}
balancedName = 'BALANCED PORTFOLIO'

emerging = {'XEC.TO': 0.8, 'XBB.TO': 0.2}
emergingName = 'EMERGING MARKETS PORTFOLIO'

international = {'XAW.TO': 0.8, 'XBB.TO': 0.2}
internationalName = 'INTERNATIONAL EQUITIES PORTFOLIO'

crisis = {'XSB.TO': 1}
crisisName = 'CRISIS 100% ST BONDS PORTFOLIO'

mpList = [balanced, emerging, international,crisis]
mpName = [balancedName, emergingName, internationalName, crisisName]

bt.performance_comparison(mpList, mpName)



# Portfolios Performance Summary



# User Interace Menu
    
while (1):    
    print()
    print('■ MODEL PORTFOLIO SELECTION\n')
    print(helper.INDENT + '1. ' + balancedName)
    print(helper.INDENT + '2. ' + emergingName)
    print(helper.INDENT + '3. ' + internationalName)
    print(helper.INDENT + '4. ' + crisisName)
    print()
    print('\t\t0. EXIT')
    
    port_choice = input('>> ')
    
    if port_choice == '0':
        sys.exit()
    
    elif port_choice == '1':
        name = "SELECTED PORTFOLIO :: " + balancedName
        helper.print_header(name)
        pt.get_description(balanced)    
    elif port_choice == '2':
        name = "SELECTED PORTFOLIO :: " + emergingName
        helper.print_header(name)
        pt.get_description(emerging)
    elif port_choice == '3':
        name = "SELECTED PORTFOLIO :: " + internationalName    
        helper.print_header(name)
        pt.get_description(international)
    elif port_choice == '4':
        name = "SELECTED PORTFOLIO :: " + crisisName        
        helper.print_header(name)
        pt.get_description(crisis)
    
    print()
    print("PROCEED? [Y/N]")
    proceed = input('>> ')
    
    if proceed == 'Y' or proceed == 'y':        
    
        allocation = {
                    '1': balanced,
                    '2': emerging,
                    '3': international,
                    '4': crisis}
        
        rb.rebalancing(allocation[port_choice])           
    
    elif proceed == 'N' or proceed == 'n':
        continue
        
 
# Portfolio Selection

# Portfolio Infomation

# Rebalancing Calculation

# Output Summary