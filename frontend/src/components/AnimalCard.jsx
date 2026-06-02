// Reusable animal card used on the dashboard.
import { Link } from "react-router-dom";

function AnimalCard({ animal, onToggleFavorite }) {
  return (
    <article className="card animal-card">
      <div>
        <h3>{animal.name}</h3>
        <p>{animal.species} {animal.breed ? `• ${animal.breed}` : ""}</p>
        <p>Status: <strong>{animal.status}</strong></p>
      </div>
      <div className="card-actions">
        <button onClick={() => onToggleFavorite(animal)}>
          {animal.is_favorite ? "★ Favorited" : "☆ Favorite"}
        </button>
        <Link className="button secondary" to={`/animals/${animal.id}`}>View</Link>
      </div>
    </article>
  );
}

export default AnimalCard;
