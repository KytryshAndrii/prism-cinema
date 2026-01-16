import { useState } from "react";
import {
  useGetActorEntityQuery,
  useGetDirectorEntityQuery,
  useGetGenreEntityQuery,
} from "../../../api/authApi";

export type EntityType = "cast" | "genres" | "directors";

export const useEntityModal = () => {
  const [selectedEntity, setSelectedEntity] = useState<{
    name: string;
    type: EntityType;
  } | null>(null);

  const [open, setOpen] = useState(false);

  const handleOpen = (name: string, type: EntityType) => {
    setSelectedEntity(null); 
    setOpen(true);
    setTimeout(() => {
      setSelectedEntity({ name, type });
    }, 0);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedEntity(null);
  };

  const actorQuery = useGetActorEntityQuery(
    selectedEntity?.type === "cast" ? selectedEntity.name : "",
    { skip: selectedEntity?.type !== "cast" }
  );

  const directorQuery = useGetDirectorEntityQuery(
    selectedEntity?.type === "directors" ? selectedEntity.name : "",
    { skip: selectedEntity?.type !== "directors" }
  );

  const genreQuery = useGetGenreEntityQuery(
    selectedEntity?.type === "genres" ? selectedEntity.name : "",
    { skip: selectedEntity?.type !== "genres" }
  );

  let entityData = null;

   switch (selectedEntity?.type) {
        case "cast":
            entityData = actorQuery.data;
            break;

        case "directors":
            entityData = directorQuery.data;
            break;

        case "genres":
            entityData = genreQuery.data;
            break;

        default:
            entityData = null;
    }
  return {
    open,
    modalTitle: selectedEntity?.name || "",
    entityData,
    handleOpen,
    handleClose,
    isLoading:
      actorQuery.isFetching ||
      directorQuery.isFetching ||
      genreQuery.isFetching,
  };
};
