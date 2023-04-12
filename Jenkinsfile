@Library('global-libs') _

pipeline {

  agent {

    kubernetes {
      containerTemplate(name: 'kaniko', image: 'gcr.io/kaniko-project/executor:debug', command: 'sleep', args: '99d')
    }
  }

  stages {

    stage('Login credentials') {
        steps {
            script {
                //gitlab_docker.login()
              withCredentials([usernamePassword(credentialsId: 'gitlab-registry', usernameVariable: 'USERNAME', passwordVariable: 'TOKEN')]) {
                sh '''               
                  echo "{\"auths\":{\"registry.gitlab.com\":{\"username\":\"$USERNAME\",\"password\":\"$TOKEN\"}}}" > /kaniko/.docker/config.json
                '''
              }
            }
        }     
    }
    stage('Build & Push') {
        steps {
            script {
              sh '''
                /kaniko/executor --context app/ \
                  --dockerfile Dockerfile \
                  --cache \
                  --build-arg CI_COMMIT_REF_SLUG=${GIT_BRANCH} \
                  --build-arg CI_COMMIT_TAG=${GIT_TAG} \
                  --build-arg CI_COMMIT_SHORT_SHA=${GIT_COMMIT} \
                  --destination registry.gitlab.com/dev-ops-tom/test \
              '''
            }
        }     
    }       
  } 
}
