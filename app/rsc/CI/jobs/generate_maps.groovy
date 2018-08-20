job('{{DEFAULT_PATH}}/generate-maps-{{MAP_TYPE}}'){
    scm {
        git {
            remote {
                url({{FUN}})
            }
        branch('{{BRANCH}}')
        }
    }
    triggers{
        scm('*/15 * * * *')
    }
    steps{
        shell('cd {{ARTIFACT_REPO_PATH}}; rm {{MAP_TYPE}}* || true')
        shell('cd {{PATH}}/scripts; python {{SCRIPT}}')
        shell('cp {{PATH}}/PNG/{{MAP_TYPE}}* {{ARTIFACT_REPO_PATH}}')
        shell('rm {{PATH}}/PNG/{{MAP_TYPE}}*')
    }
}
