
question_interacitve <- function(question) {
	

  test_question <- question
  

  
    machine(test_question)

}
  
  machine<-function(test_question){
    
    library(tm)
    
    data_location <- getwd()
    questions <- data.frame(read.csv(paste(data_location, "/questions.csv", sep = "")))
    questions[,1] <- as.character(questions[,1])
    questions[,2] <- as.character(questions[,2])
    questions[,3] <- as.character(questions[,3])
    
    answers <- data.frame(read.csv(paste(data_location, "/answers.csv", sep = "")))
    answers[,1] <- as.character(answers[,1])
    answers[,2] <- as.character(answers[,2])
    
    answers_generic <- data.frame(read.csv(paste(data_location, "/Generic Answers.csv", sep = "")))
    answers_generic[,2] <- as.character(answers_generic[,2])
    answers_generic[,3] <- as.character(answers_generic[,3])
    
    test_cutoff <- 1149
    questions_train <- questions[1:test_cutoff,]
    questions_test <- questions[test_cutoff+1:1159,]
    answers_train <- answers[1:test_cutoff,]
    answers_test <- answers[test_cutoff+1:1159,]
    
    corpus <- Corpus(VectorSource(c(questions_train[,2],test_question)))
    corpus <- tm_map(corpus, removeNumbers)
    corpus <- tm_map(corpus, removePunctuation)
    corpus <- tm_map(corpus, content_transformer(tolower))
    corpus <- tm_map(corpus, removeWords, stopwords("english"))
    corpus <- tm_map(corpus, removeWords, stopwords("english"))
    corpus <- tm_map(corpus, stemDocument,language="english")
    corpus <- tm_map(corpus, stripWhitespace)
    
    dtm <- DocumentTermMatrix(corpus, control = list(wordlengths = c(3, Inf), bounds = list(global = c(3,300))))
    dtm_tfxidf <- weightTfIdf(dtm)
    mat <- as.matrix(dtm_tfxidf)
    
    
    library(proxy)
    #cross_dist <- dist(mat, method = "cosine")
    
    distances <- NULL
    for(i in 1:(nrow(mat)-1))
    {
      distances <- rbind(distances,dist(rbind(mat[i,],mat[1150,]), method = "cosine"))
    }
    
    test_question
    answer <- answers[which(distances==min(distances)),2]
    if(sum(answers[which(distances==min(distances)),21]) > 0)
    {
    	generic_vec <- colSums(answers[which(distances==min(distances)),3:20]) > 0
    	answer_vec <- answers_generic[generic_vec,3]
    	answer <- paste(answer_vec, sep = "\n\n\n\t")
    }
    
    	
    print(answer)   
  }
  

