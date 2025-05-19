<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo y título -->
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
          {{ title }}
        </h2>
        <p v-if="subtitle" class="mt-2 text-sm text-gray-600">
          {{ subtitle }}
        </p>
      </div>

      <!-- Contenido del formulario -->
      <div class="mt-8 bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
        <slot></slot>
      </div>

      <!-- Enlaces adicionales -->
      <div v-if="showLinks" class="text-center text-sm">
        <slot name="links">
          <p class="text-gray-600">
            {{ linkText }}
            <router-link :to="linkTo" class="font-medium text-indigo-600 hover:text-indigo-500">
              {{ linkLabel }}
            </router-link>
          </p>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout',
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      default: ''
    },
    linkText: {
      type: String,
      default: ''
    },
    linkLabel: {
      type: String,
      default: ''
    },
    linkTo: {
      type: [String, Object],
      default: '/'
    },
    showLinks: {
      type: Boolean,
      default: true
    }
  }
}
</script>
