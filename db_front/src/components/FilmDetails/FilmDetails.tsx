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
  RowRating,
  PgBadge,
  ActionsPanel,
  Underline,
  ActionSwitch,
  ActionSwitchButton,
  LikeButton,
  RateStar,
  RatingWrapper,
  GeneralDataWrapper,
} from "./styles";
import { useFilmDetailsRender } from "./useFilmDetailsRender";
import { Skeleton } from "@mui/material";
import type { AppState } from "../../store/store";
import { useSelector } from "react-redux";
import { HeartIcon } from "../../icons/icons";
import { useEntityModal, type EntityType } from "./EntityModal/useEntityModal";
import EntityModal from "./EntityModal/EntityModal";

const FilmDetails: React.FC = () => {
  const {movieMeta, toggleLikeMovie} = useFilmDetailsRender();
  const user = useSelector((state: AppState) => state.user);
  const [view, setView] = useState<"movie" | "trailer">("trailer");
  const [activeTab, setActiveTab] = useState<EntityType>("cast");

  const {
    open,
    modalTitle,
    entityData,
    handleOpen,
    handleClose,
  } = useEntityModal();

  return (
    <PageWrapper>
      <BackdropWrapper>
        <BackdropImage src={movieMeta.backdrop!} />
        <BackdropGradient />
      </BackdropWrapper>

      <ContentWrapper>
        <InfoGrid>  
            <Poster src={movieMeta.poster!} />
          <div>
            <Title>{movieMeta.title}</Title>
            <RowRating>
              <RatingWrapper><RateStar/> <strong>{movieMeta.rating}/10</strong></RatingWrapper>
              <PgBadge pg={movieMeta.pg}>{movieMeta.pg}</PgBadge>
            </RowRating>
            {movieMeta.description ? (
              <GeneralDataWrapper>
                <Description>{movieMeta.description}</Description>
                <Description>
                  Release: <strong>{movieMeta.release_date}</strong>
                </Description>
              </GeneralDataWrapper>
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
              {movieMeta.cast.length || movieMeta.description.length || movieMeta.directors.length ? 
              (
                <>{(activeTab === "cast" ? movieMeta.cast : activeTab === "directors" ? movieMeta.directors : movieMeta.genres).map(
                (item) => (
                  <Chip
                    key={item}
                    onClick={() => handleOpen(item, activeTab)}
                    >
                    {item}
                  </Chip>
                ))}
                </>
              ):(
                <Skeleton variant="text" width={300} height={50} sx={{ bgcolor: 'grey.900' }}/>
              )
              }
            </ChipsRow>
            <EntityModal
              open={open && !!entityData}
              onClose={handleClose}
              title={modalTitle}
              data={entityData}
            />
          </div>
        </InfoGrid>
        <TrailerWrapper>
          {view === "trailer" || !user.isUserSubscribed ? (
            movieMeta.trailerUrl ? (
              <iframe
                src={movieMeta.trailerUrl}
                title="Movie trailer"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                loading="lazy"
                style={{ width: "100%", height: "100%", border: "none" }}
              />
            ) : (
              <Skeleton variant="text" sx={{ height: "100%", bgcolor: "grey.900" }} />
            )
            ) : (
              <iframe
                src="https://example.com/actual_movie.mp4"
                title="Movie stream"
                allowFullScreen
                loading="lazy"
                style={{ width: "100%", height: "100%", border: "none" }}
              />
            )}
        </TrailerWrapper>
        {user.isUserSubscribed && (
          <ActionsPanel>
            <LikeButton active={movieMeta.isLiked} onClick={toggleLikeMovie}>
              <HeartIcon />
                Like
            </LikeButton>

            <Underline />

            <ActionSwitch>
              <ActionSwitchButton
                active={view === "movie"}
                onClick={() => setView("movie")}
              >
                MOVIE
              </ActionSwitchButton>
              <ActionSwitchButton
                active={view === "trailer"}
                onClick={() => setView("trailer")}
              >
                TRAILER
              </ActionSwitchButton>
            </ActionSwitch>
          </ActionsPanel>
        )}

      </ContentWrapper>
    </PageWrapper>
  );
};

export default FilmDetails;
