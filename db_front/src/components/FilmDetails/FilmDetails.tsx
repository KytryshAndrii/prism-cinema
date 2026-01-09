import type React from "react";
import { useState } from "react";
import {
  PageWrapper,
  BackdropWrapper,
  BackdropImage,
  BackdropGradient,
  ContentWrapper,
  InfoGrid,
  Poster,
  Title,
  Description,
  ToggleRow,
  ToggleLabel,
  ChipsRow,
  Chip,
  TrailerWrapper,
} from "./styles";
import { useFilmDetailsRender } from "./useFilmDetailsRender";

const FilmDetails: React.FC = () => {
  const film = useFilmDetailsRender();
  const [activeTab, setActiveTab] = useState<"cast" | "genres">("cast");

  return (
    <PageWrapper>
      <BackdropWrapper>
        <BackdropImage src={film.backdrop} />
        <BackdropGradient />
      </BackdropWrapper>

      <ContentWrapper>
        <InfoGrid>
          <Poster src={film.poster} />

          <div>
            <Title>{film.title}</Title>
            <Description>{film.description}</Description>

            <ToggleRow>
              <ToggleLabel
                active={activeTab === "cast"}
                onClick={() => setActiveTab("cast")}
              >
                CAST
              </ToggleLabel>
              <ToggleLabel
                active={activeTab === "genres"}
                onClick={() => setActiveTab("genres")}
              >
                GENRES
              </ToggleLabel>
            </ToggleRow>

            <ChipsRow>
              {(activeTab === "cast" ? film.cast : film.genres).map(
                (item) => (
                  <Chip key={item}>{item}</Chip>
                )
              )}
            </ChipsRow>
          </div>
        </InfoGrid>
        <TrailerWrapper>
          <iframe
            src={film.trailerUrl}
            title="Movie trailer"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            loading="lazy"
            style={{ width: "100%", height: "100%", border: "none" }}
          />
        </TrailerWrapper>
      </ContentWrapper>
    </PageWrapper>
  );
};

export default FilmDetails;
