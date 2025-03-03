<script setup>

</script>

<template>
<span class="openbtn"></span>

<div class="sidenav">
    <div>
        <h1>Vibe</h1>
        <button class="closebtn"></button>
        <button class="newbtn">New chat</button>

        <h2>Today</h2>
        <a href="#">Last chat</a>
    </div>
</div>
</template>

<style scoped>
/* Button to open nav menu */
span.openbtn {
    cursor: pointer;
}

/* Nav menu */
.sidenav {
    height: 100%;       /* 100% Full-height */
    width: 300px;       /* Decide width */
    position: fixed;    /* Stay in place */
    z-index: 1;         /* Stay on top */
    top: 0;             /* Stay at the top */
    left: 0;            /* Nav on left side */
    background-color: #2a2a2a;    /* Black*/
    overflow-x: hidden;             /* Disable horizontal scroll */
    padding-top: 60px;              /* Place content 60px from the top */
    transition: 0.5s;               /* 0.5 second transition effect to slide in the sidenav */
}

.sidenav div {
    margin: auto;
    width: 85%;
}

/* Nav menu button for new chat */
.sidenav .newbtn {
    height: 40px;
    width: 120px;
    font-weight: bold;
    background-image: linear-gradient(to right, #c957b4, #395cdb);
    font-size: large;
    border: none;
    border-radius: 10px;
    color: white;
    cursor: pointer;
    margin: 30px 0px 25px 0px;
}

/* Button to close nav menu */
.sidenav .closebtn {
    height: 20px;
    width: 20px;
    position: absolute;
    top: 5px;
    right: 25px;
    font-size: 36px;
    margin-left: 50px;
    background: url(../assets/icon.png);
    border: none;
}

/* Title */
.sidenav h1 {
    color: white;
    position: absolute;
    top: 10px;
    margin: auto;
    font-size: 45px;
}

/* Date for older chats */ 
.sidenav h2 {
    color: white;
}

/* Nav menu links */
.sidenav a {
    padding: 6px 6px 6px 16px;
    text-decoration: none;
    font-size: 20px;
    color: #818181;
    display: block;
    transition: 0.3s;
    text-align: left;
    border-radius: 10px;
    width: 100%;
    margin: auto;
} 

/* Change color when hovering over nav link */
.sidenav a:hover {
    color: #f1f1f1;
}

</style>