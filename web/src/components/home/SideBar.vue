<template>
  <div class="sidebar">
    <h2>APSocial</h2>
    <ul class="nav-list">
      <li>
        <router-link to="/"><i class="fas fa-home"></i> ACASĂ</router-link>
      </li>
      <li>
        <router-link to="/search"><i class="fas fa-search"></i> CAUTĂ</router-link>
      </li>
      <li>
        <router-link to="/chat"><i class="fas fa-comments"></i> CHAT</router-link>
      </li>
      <li>
        <router-link to="/notifications"><i class="fas fa-bell"></i> NOTIFICĂRI</router-link>
      </li>
      <li>
        <router-link to="/profile"><i class="fas fa-user"></i> PROFIL</router-link>
      </li>
    </ul>
    <div class="settings">
      <router-link to="/settings" class="settings-link">
        <i class="fas fa-cog">
        </i>
          SETĂRI
      </router-link>
    </div>
  </div>

  <div class="main-content">
    <router-view></router-view>
  </div>
</template>

<style scoped>
h2 {
  color: #f2f2f2;
}

/* Contenitorul principal */
.sidebar {
  width: 220px;
  background-color: #070606;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 100vh;
  border-right: 2px solid white;
  position: fixed;
}

.main-content {
  margin-left: 220px;
  padding: 20px;
  background-color: #1a1a1a;
  color: white;
  height: 100vh;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  padding: 0;
}

.nav-list li {
  margin-bottom: 20px;
}

.nav-list a {
  text-decoration: none;
  color: white;
  font-size: 18px;
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.nav-list a:hover {
  background-color: #333;
}

.nav-list a i {
  margin-right: 10px;
}

/* Sidebar */
.sidebar {
  width: 220px;
  background-color: #070606;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column; /* Afișează elementele vertical */
  height: 100vh;
  border-right: 2px solid white;
  position: fixed; /* Sidebar fixat pe partea stângă */
}

/* Secțiunea Setări */
.settings {
  margin-top: auto; /* Poziționează secțiunea în partea de jos */
  padding-top: 20px;
  border-top: 1px solid #333; /* Linie de separare */
}

.settings-link {
  display: flex;
  align-items: center;
  color: white;
  text-decoration: none;
  font-size: 18px;
  margin-bottom: 3rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.settings-link:hover {
  background-color: #333; /* Evidențiază link-ul la hover */
  padding: 10px; /* Crește padding-ul pe hover */
}


.settings-link i {
  margin-right: 10px; /* Spațiere între iconiță și text */
}


/* Conținut principal */
.main-content {
  flex-grow: 1; /* Ocupă tot spațiul disponibil în dreapta */
  margin-left: 250px; /* Asigură spațiu pentru sidebar */
  background-color: #1a1a1a;
  color: white;
}

</style>
