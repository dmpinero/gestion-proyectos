<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          ¡Registro Exitoso!
        </h2>
        <div class="mt-4 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
          <div class="flex">
            <div class="py-1">
              <svg class="h-6 w-6 text-green-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div>
              <p class="font-bold">Tu cuenta ha sido creada correctamente</p>
              <p class="text-sm">Ahora puedes iniciar sesión con tus credenciales.</p>
            </div>
          </div>
        </div>
      </div>
      <div class="mt-8">
        <div class="text-center">
          <p>Serás redirigido a la página de inicio de sesión en <span class="font-bold">{{ countdown }}</span> segundos.</p>
        </div>
        <div class="mt-4">
          <button 
            @click="goToLogin" 
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Ir a Iniciar Sesión
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'RegisterSuccessView',
  setup() {
    const router = useRouter();
    const countdown = ref(5);
    let timer = null;

    const goToLogin = () => {
      // Obtener el email de los parámetros de la URL
      const email = router.currentRoute.value.query.email || '';
      
      // Redirigir a la página de login con el email como parámetro
      router.push({
        name: 'Login',
        query: { 
          email,
          registered: 'true'
        }
      });
    };

    onMounted(() => {
      // Iniciar el contador regresivo
      timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
          goToLogin();
        }
      }, 1000);
    });

    onBeforeUnmount(() => {
      // Limpiar el timer cuando el componente se desmonta
      if (timer) {
        clearInterval(timer);
      }
    });

    return {
      countdown,
      goToLogin
    };
  }
};
</script>
