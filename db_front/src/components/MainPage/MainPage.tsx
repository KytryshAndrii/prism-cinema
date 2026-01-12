import React from "react";
import {
  Container,
  Heading,
  FilmsGrid,
  FilmCard,
  FilmImage,
  FilmInfo,
  FilmTitle
} from "./styles";
import { useMainPageFilmsRender } from "./useMainPageFilmsRender";
import { useNavigate } from "react-router-dom";
import { CircularProgress, Typography } from "@mui/material";
import { useSelector } from "react-redux";
import type { AppState } from "../../store/store";
import { useDispatch } from "react-redux";
import { setFilm } from "../../store/filmSlice";
import type { tFilmMetaData } from "./types";

const MainPage: React.FC = () => {
  const dispatch = useDispatch();
  const { films, isLoading, isError } = useMainPageFilmsRender();
  const { isLoggedIn, login } = useSelector((state: AppState) => state.user);

  const navigate = useNavigate();
  const handleFilmClick = (film: tFilmMetaData) => {
    dispatch(setFilm({
      id: film.id,
      name: film.title,
      poster: film.imageUrl,
      preview_poster: film.previewImg
    }));
    navigate(`/film_entity`);
  };

  return (
    <Container>
      <Heading>{isLoggedIn
          ? `Welcome back, ${login?.toUpperCase()}. Here's what we've been watching...`
          : "Here’s what we’ve been watching..."}</Heading>

      {isLoading && <CircularProgress />}
      {isError && <Typography color="error">Failed to load movies.</Typography>}

      <FilmsGrid>
        {films.map((film) => (
          <FilmCard key={film.id} onClick={() => handleFilmClick(film)}>
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
