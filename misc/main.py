"""
AUTOMATIC POSITION CALCULATOR VER.3
"""

import sys


import portfolios as pt
import helper
import rebalancing as rb
import backtesting as bt

version = 3

helper.print_title('\t'*36 + "AUTOMATIC POSITION CALCULATOR - VERSION " + str(version))

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

# User Interace Menu

while (1):
    helper.print_header('MAIN MENU')
    print(helper.INDENT + '1. MODEL PORTFOLIO PERFORMANCE COMPARISON')
    print(helper.INDENT + '2. PORTFOLIO SELECTION FOR REBALANCING')
    print(helper.INDENT + '3. ASSET ALLOCATION PORTFOLIO BACKTESTING')
    print()
    print(helper.INDENT + '0. Exit')

    action = input('>> ')

    if action == '0':
        sys.exit()

    elif action == '1':
        helper.print_header('MODEL PORTFOLIO PERFORMANCE COMPARISON')
        bt.performance_comparison(mpList, mpName)
        print()
        print('END OF DATA')
        print()
        print("PRESS ANYTHING TO GO BACK TO MAIN MENU.")
        action = input('>> ')
        continue

    if action == '2':
        helper.print_header('MODEL PORTFOLIO SELECTION')
        print(helper.INDENT + '1. ' + balancedName)
        print(helper.INDENT + '2. ' + emergingName)
        print(helper.INDENT + '3. ' + internationalName)
        print(helper.INDENT + '4. ' + crisisName)
        print()
        print(helper.INDENT + '0. EXIT')

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
        print("PROCEED WITH SELECTED PORTFOLIO FOR REBALANCING? [Y/N]")
        proceed = input('>> ')

        if proceed == 'Y' or proceed == 'y':
            allocation = {
                        '1': balanced,
                        '2': emerging,
                        '3': international,
                        '4': crisis}
            rb.rebalancing(allocation[port_choice])

        else:
            continue


