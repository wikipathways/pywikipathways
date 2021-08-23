def list_pathways(organism=""):
    res = wikipathways_get('listpathways', {'organism' = organism})
    pass

# listPathways <- function(organism="") {
#     res <- wikipathwaysGET('listPathways', list(organism=organism))
#     if(length(res$pathways) == 0){
#         message("No results")
#         return(data.frame())
#     }
#     #make into list of list (like other web service responses)
#     res.pathways <- lapply(res$pathways, as.list)
#     res.df <- suppressWarnings(data.table::rbindlist(res.pathways, fill = TRUE))
#     res.df$revision <- vapply(res.df$revision, as.integer, integer(1)) 
#     return(res.df)
# } 
