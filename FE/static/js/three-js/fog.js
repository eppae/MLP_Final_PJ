import * as THREE from 'three';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x212529); // 컬러 바꾸기
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0,0,5)
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
const container = document.getElementById('threejs-container')
container.appendChild(renderer.domElement);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(0, 0, 1);
scene.add(directionalLight);

const geometry01 = new THREE.BoxGeometry(1,1,1); // x, y, z
const material01 = new THREE.MeshStandardMaterial({
    color:0x79E5CB
})
const obj01 = new THREE.Mesh(geometry01,material01)
obj01.position.x = -2;
scene.add(obj01)

function animate() {
    requestAnimationFrame(animate);
    // Your animation logic goes here
    obj01.rotation.y += 0.01;

    // const scrollPosition = window.scrollY;
    // if (scrollPosition > window.innerHeight) {
    //     obj01.visible = false;  // Hide the object
    // } else {
    //     obj01.visible = true;  // Show the object
    // }

    renderer.render(scene, camera);
}
animate();

function onWindowResize(){
    camera.aspect = window.innerWidth / window.innerHeight; // 종횡비 가변 처리
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
}
window.addEventListener('resize', onWindowResize);

window.addEventListener('scroll', function () {
    const scrollPosition = window.scrollY;
    const containerHeight = container.clientHeight;

    // Check if the scroll position is below the container's height
    if (scrollPosition > containerHeight) {
        container.style.display = 'none';  // Hide the container
    } else {
        container.style.display = 'block';  // Show the container
    }
});