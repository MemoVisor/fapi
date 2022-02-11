node {
  ansiColor('xterm') {

    stage('scm') {
      checkout(scm)
    }

    stage('secrets') {
      sh(script: "echo Secret=http://ea92428125c1464caad > .env")
      sh(script: "echo Secret2=http://ea92428125c1464caad828 >> .env")
    }

    stage('build') {
      sh(script: "docker build --force-rm --no-cache=${env.BUILD_CLEAN} --tag=${image_name} -f ci/docker/Dockerfile .")
    }

    stage('run') {
      sh(script: "docker stop ${container_name} || true")
      sh(script: "docker rm ${container_name} || true")
      sh(script: """
        docker run \
          --name ${container_name} \
          --restart always \
          --detach \
          --cpu-shares 405 \
          --privileged \
          --env APP_ENV=${app_env} \
          --expose 80 \
          --publish 80:80 \
          ${image_name}
      """)
    }
    stage('docker clean') {
      sh(script: "docker system prune --volumes -f")
    }
  }
}