$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var taskInfo = button.data('whatever').split(',')
  var taskTitle = taskInfo[0]
  var taskId = taskInfo[1]

  var modal = $(this)

  modal.find('.modal-body input').val("タスク名："+ taskTitle)
  modal.find('.modal-footer input').val(taskId)
})

$('#editTaskModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var taskInfo = button.data('whatever').split(',')
  var taskTitle = taskInfo[0]
  var taskId = taskInfo[1]
  var taskLimit = taskInfo[2]

  var modal = $(this)

  modal.find('.modal-body input#task-name').val(taskTitle)
  modal.find('.modal-body input#task-limit').val(taskLimit)
  modal.find('.modal-footer input#task-id').val(taskId)
})
