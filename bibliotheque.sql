-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : dim. 21 sep. 2025 à 20:39
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `bibliotheque`
--

-- --------------------------------------------------------

--
-- Structure de la table `emprunts`
--

DROP TABLE IF EXISTS `emprunts`;
CREATE TABLE IF NOT EXISTS `emprunts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `utilisateur_id` int NOT NULL,
  `livre_id` int NOT NULL,
  `date_emprunt` date NOT NULL DEFAULT (curdate()),
  `date_retour_prevue` date NOT NULL,
  `date_retour_effective` date DEFAULT NULL,
  `statut` enum('en_cours','rendu','retard') COLLATE utf8mb4_unicode_ci DEFAULT 'en_cours',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_utilisateur` (`utilisateur_id`),
  KEY `idx_livre` (`livre_id`),
  KEY `idx_statut` (`statut`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `emprunts`
--

INSERT INTO `emprunts` (`id`, `utilisateur_id`, `livre_id`, `date_emprunt`, `date_retour_prevue`, `date_retour_effective`, `statut`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2024-01-15', '2024-02-15', '2025-09-21', 'rendu', '2025-09-21 17:51:14', '2025-09-21 19:37:31'),
(2, 2, 2, '2024-01-20', '2024-02-20', '2025-09-21', 'rendu', '2025-09-21 17:51:14', '2025-09-21 19:04:22'),
(3, 1, 3, '2024-01-25', '2024-02-25', NULL, 'en_cours', '2025-09-21 17:51:14', '2025-09-21 17:51:14'),
(4, 2, 4, '2025-09-21', '2025-10-21', NULL, 'en_cours', '2025-09-21 19:04:35', '2025-09-21 19:04:35'),
(5, 5, 6, '2025-09-21', '2025-10-21', NULL, 'en_cours', '2025-09-21 19:36:50', '2025-09-21 19:36:50');

-- --------------------------------------------------------

--
-- Structure de la table `livres`
--

DROP TABLE IF EXISTS `livres`;
CREATE TABLE IF NOT EXISTS `livres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `titre` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `auteur` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `isbn` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `genre` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `annee_publication` int DEFAULT NULL,
  `disponible` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `isbn` (`isbn`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `livres`
--

INSERT INTO `livres` (`id`, `titre`, `auteur`, `isbn`, `genre`, `annee_publication`, `disponible`, `created_at`, `updated_at`) VALUES
(1, 'Le Petit Prince', 'Antoine de Saint-Exupéry', '978-2070408504', 'Fiction', 1943, 0, '2025-09-21 17:51:14', '2025-09-21 17:51:14'),
(2, '1984', 'George Orwell', '978-0451524935', 'Science-fiction', 1949, 0, '2025-09-21 17:51:14', '2025-09-21 17:51:14'),
(3, 'L\'Étranger', 'Albert Camus', '978-2070360024', 'Philosophie ', 1942, 0, '2025-09-21 17:51:14', '2025-09-21 19:03:39'),
(4, 'Harry Potter à l\'école des sorciers', 'J.K. Rowling', '978-2070541270', 'Fantasy', 1997, 0, '2025-09-21 17:51:14', '2025-09-21 19:04:35'),
(6, 'L\'Étranger dal', 'Albert Camus', '978-20703600888', 'Philosophie', 1995, 0, '2025-09-21 19:36:27', '2025-09-21 19:36:50'),
(7, 'Alba l\'or et l\'amour', 'jean claude', '528998444', 'drame', 1990, 1, '2025-09-21 20:27:40', '2025-09-21 20:27:40');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs`
--

DROP TABLE IF EXISTS `utilisateurs`;
CREATE TABLE IF NOT EXISTS `utilisateurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prenom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_inscription` date DEFAULT (curdate()),
  `actif` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `utilisateurs`
--

INSERT INTO `utilisateurs` (`id`, `nom`, `prenom`, `email`, `telephone`, `date_inscription`, `actif`, `created_at`, `updated_at`) VALUES
(1, 'Dupont', 'Jean', 'jean.dupont@email.com', '0123456789', '2025-09-21', 1, '2025-09-21 17:51:14', '2025-09-21 17:51:14'),
(2, 'Martin', 'Marie', 'marie.martin@email.com', '0987654321', '2025-09-21', 1, '2025-09-21 17:51:14', '2025-09-21 17:51:14'),
(3, 'Bernard', 'Pierre', 'pierre.bernard@email.com', '0147258369', '2025-09-21', 1, '2025-09-21 17:51:14', '2025-09-21 17:51:14'),
(5, 'ANDRIATINIAINA', 'Salomon', 'salomonandriatiniaina@gmail.com', '0343405224', '2025-09-21', 1, '2025-09-21 19:15:53', '2025-09-21 19:15:53');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
