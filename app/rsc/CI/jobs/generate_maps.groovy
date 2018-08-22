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
        shell('cp {{ARTIFACT_REPO_PATH}}/{{SOURCE_MAP_TYPE}}* {{PATH}}')
        shell('cd {{PATH}}/scripts; python {{SCRIPT}}')
        shell('cd {{ARTIFACT_REPO_PATH}}; rm {{MAP_TYPE}}* || true')
        shell('cp {{PATH}}/PNG/{{MAP_TYPE}}* {{ARTIFACT_REPO_PATH}}')
        shell('rm {{PATH}}/PNG/{{MAP_TYPE}}*')
    }
}
