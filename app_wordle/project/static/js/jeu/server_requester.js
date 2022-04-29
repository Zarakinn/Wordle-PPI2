const host = window.location.host; // Récupère l'url de la page
const protocol = window.location.protocol; // Récupère l'url de la page
const est_dans_dict_api_endpoint = "api/estValideMot";
const get_score_api_endpoint = "api/getScore";

const est_dans_dictionnaire = (mot) => {
    const url = `${protocol}//${host}/${est_dans_dict_api_endpoint}/${mot}`;

    // Abandon de la requête au bout de 5 secondes
    const controller = new AbortController()
    setTimeout(() => controller.abort(), 5000)

    return fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
        signal: controller.signal
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(new Error("not ok response"));
            }
        })
        .then(response => {
            if (response.status_custom === "error") {
                return Promise.reject(new Error("Erreur interne au serveur ⏩" + response.error_message));
            }
            return response.estValide;
        })
        .catch(error => {
            return Promise.reject(new Error(error.message));
        });
};

const get_score_fin_partie = () => {
    const url = `${protocol}//${host}/${get_score_api_endpoint}`;

    // Abandon de la requête au bout de 5 secondes
    const controller = new AbortController()
    setTimeout(() => controller.abort(), 5000)

    return fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
        signal: controller.signal
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return Promise.reject(new Error("not ok response"));
            }
        })
        .then(response => {
            if (response.status_custom === "error") {
                return Promise.reject(new Error("Erreur interne au serveur ⏩ " + response.error_message));
            }
            if (response.status_custom === "not_logged_in") {
                return "Connectez-vous pour voir votre score !";
            }
            return response.score;
        })
        .catch(error => {
            return Promise.reject(new Error("Mauvaise réponse du serveur ⏩ " + error.message));
        });

}

export default {
    est_dans_dictionnaire,
    get_score_fin_partie
}