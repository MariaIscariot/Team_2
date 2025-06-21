import { useState } from 'react'
import Subjects from './components/Subjects/Subjects'
import MainBody from './components/MainBody/MainBody'
import './App.css'

function App() {  

  return (
    <div className='app'>
      <Subjects/>
      <MainBody/>
    </div>
  )
}

export default App
