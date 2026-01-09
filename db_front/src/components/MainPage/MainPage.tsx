import React from 'react';
import {
  Container,
  Heading,
  FilmsGrid,
  FilmCard,
  FilmImage,
  FilmInfo,
  FilmTitle
} from './styles';
import { useMainPageFilmsRender } from './useMainPageFilmsRender';
import { useNavigate } from "react-router-dom";

const MainPage: React.FC = () => {
  const films = useMainPageFilmsRender();
  const navigate = useNavigate();
  const handleFilmClick = (id: number) => {
    console.log(`Clicked film ID: ${id}`);
    navigate("/film_entity")
    // TODO: implement navigate(`/films/${id}`)
  };

  return (
    <Container>
      <Heading>Here’s what we’ve been watching...</Heading>
      <FilmsGrid>
        {films.map((film) => (
          <FilmCard key={film.id} onClick={() => handleFilmClick(film.id)}>
            <FilmImage src={film.imageUrl} alt={film.title} />
            <FilmInfo>
              <FilmTitle>{film.title}</FilmTitle>
            </FilmInfo>
          </FilmCard>
        ))}
      </FilmsGrid>
    </Container>
  );
};

export default MainPage;
