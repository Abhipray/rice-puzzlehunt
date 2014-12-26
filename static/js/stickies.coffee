jQuery ->
    console.log('Script ran')
    $('#add-button').click (e) =>
        e.preventDefault()
        fields = [$('#input-text')]
        for field in fields
            if field.val().trim() == ""
                alert('Missing input')
                return

        postData =
            'attempt': fields[0].val()
            'puzzleNum' : puzzleNum
        if confirm('Are you sure about your answer:\n' + postData['attempt'])
            $.ajax
                url: '/puzzle'
                type: 'POST'
                data: 'data': JSON.stringify(postData)
                success: (data) ->
                    response = JSON.parse(data)
                    success = response['success']
                    correctness = response['correctness']
                    note = response['attempt']
                    id = response['id']
                    if correctness and not success
                        html = $("
                        <div class='alert alert-info' data-id='#{id}'>
                        <h4>You already got it right!</h4>
                        <h5>#{note}</h5>
                        <h5>#{id}</h5>
                        </div>")
                    else if not correctness and not success
                        html = $("
                        <div class='alert alert-danger' data-id='#{id}'>
                        <h4>You have run out of attempts!</h4>
                        <h5>#{note}</h5>
                        <h5>#{id}</h5>
                        </div>")
                    else if success and correctness
                        html = $("
                        <div class='alert alert-success' data-id='#{id}'>
                        <h4>Correct answer!</h4>
                        <h5>#{note}</h5>
                        <h5>#{id}</h5>
                        </div>")
                        $('#name_score').text(response['team_name'] + ' | ' + response['team_score'])
                    else if success and not correctness
                        html = $("
                        <div class='alert alert-danger' data-id='#{id}'>
                        <h4>Wrong answer!</h4>
                        <h5>#{note}</h5>
                        <h5>#{id}</h5>
                        </div>")
                    $('#attempts').prepend(html)
                    html.hide().slideDown(500)
                    html.children('button[class="close"]').click(deleteSticky)

#deleteSticky = (e) ->
#    sticky = $(this).parent()
#    sticky_id = sticky.attr('data-id')
#    $.ajax
#        url: '/stickies/delete'
#        type: 'POST'
#        data: 'id': sticky_id
#        success: (data) ->
#            if data == 'Success!'
#                sticky.slideUp(500)