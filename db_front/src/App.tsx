import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Background from './components/Background/Background';
import HomePage from './components/HomePage/HomePage';
import NavBar from './components/NavBar/NavBar';
import MainPage from './components/MainPage/MainPage';
import FilmDetails from './components/FilmDetails/FilmDetails';
import SubscriptionsPlans from './components/SubscriptionsPlans/SubscriptionsPlans';

const App: React.FC = () => {
  return (
    <>
      <Background />
      <Router>
       <NavBar/>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/films" element={<MainPage />} />
          <Route path="/film_entity" element={<FilmDetails/>}/>
          <Route path="/subscriptions" element={<SubscriptionsPlans/>}/>
        </Routes>
      </Router>
    </>
  );
};

export default App;
