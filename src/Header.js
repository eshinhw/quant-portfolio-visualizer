import React from 'react'
import Logo from './robinhood.svg'
import './Header.css'
import { TextField } from '@mui/material'

function Header() {
  return (
    <div className='header__wrapper'>
      {/* logo */}
      <div className='header__logo'>
        <img src={Logo} width={25} />
      </div>
      {/* search bar */}
      <div className='header__search'>
        <div className='header__searchContainer'>
          <input placeholder='Search' type="text" />
        </div>
      </div>
      {/* menu items */}
      <div className='header__menuItems'>
        <a href='#'>Free Stocks</a>
        <a href='#'>Portfolio</a>
        <a href='#'>Cash</a>
        <a href='#'>Messages</a>
        <a href='#'>Account</a>

      </div>

    </div>
  )
}

export default Header