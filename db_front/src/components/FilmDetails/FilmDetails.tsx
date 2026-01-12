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
import { Skeleton } from "@mui/material";

const FilmDetails: React.FC = () => {
  const film = useFilmDetailsRender();
  const [activeTab, setActiveTab] = useState<"cast" | "genres" | "directors">("cast");

  return (
    <PageWrapper>
      <BackdropWrapper>
        <BackdropImage src={film.backdrop!} />
        <BackdropGradient />
      </BackdropWrapper>

      <ContentWrapper>
        <InfoGrid>  
            <Poster src={film.poster!} />
          <div>
            <Title>{film.title}</Title>
            {film.description ? (
              <Description>{film.description}</Description>
              ): (
              <Skeleton variant="text" width={300} height={50} sx={{ bgcolor: 'grey.900' }}/>
              )
            }

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
              <ToggleLabel
                active={activeTab === "directors"}
                onClick={() => setActiveTab("directors")}
              >
                DIRECTORS
              </ToggleLabel>
            </ToggleRow>

            <ChipsRow>
              {film.cast.length || film.description.length || film.directors.length ? 
              (
                <>{(activeTab === "cast" ? film.cast : activeTab === "directors" ? film.directors : film.genres).map(
                (item) => (
                  <Chip key={item}>{item}</Chip>
                ))}
                </>
              ):(
                <Skeleton variant="text" width={300} height={50} sx={{ bgcolor: 'grey.900' }}/>
              )
              }
            </ChipsRow>
          </div>
        </InfoGrid>
        <TrailerWrapper>
          {film.trailerUrl ? (
            <iframe
              src={film.trailerUrl}
              title="Movie trailer"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              loading="lazy"
              style={{ width: "100%", height: "100%", border: "none" }}
            />
          ) : ( 
            <Skeleton variant="text"  sx={{height:'100%', bgcolor: 'grey.900' }}/>
            )
          }
        </TrailerWrapper>
      </ContentWrapper>
    </PageWrapper>
  );
};

export default FilmDetails;
